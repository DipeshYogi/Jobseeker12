from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Jobs, AppliedJob, ShortList
from .forms import searchForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
import csv

from .notify import send_mail

def home(request):
    return render(request, 'jobskills/home.html')

def allJobs(request):
    job = Jobs.objects.order_by('-posted_date')
    page = request.GET.get('page', 1)

    paginator = Paginator(job,6)
    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        jobs = paginator.page(1)
    except EmptyPage:
        jobs = paginator.page(paginator.num_pages)


    return render(request, 'jobskills/all_jobs.html', {'jobs':jobs})


class JobCreateView(LoginRequiredMixin, CreateView):
    model = Jobs
    fields = ['title','type','req_skills','exp']
    template_name = 'jobskills/jobs_form.html'

    def form_valid(self,form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

'''
class JobDetailView(DetailView):
    model = Jobs
    template_name = 'portal/job_detail.html'
    context_object_name='jobs'
'''
@login_required
def jobdetailview(request,pk):
    jobs = Jobs.objects.get(pk=pk)
    jid = jobs.id
    is_applied = AppliedJob.objects.filter(applied_by=request.user, job_id=jid)
    is_shortlisted = ShortList.objects.filter(emp_id=request.user.id, job_id=jid)
    context = {'jobs':jobs,'is_app':is_applied, 'is_shrt':is_shortlisted}
    if request.method == 'POST':
        job_id = jid
        AppliedJob.objects.create(applied_by = request.user, job_id = jid)
        messages.success(request,f'Applied for job')
    return render(request,'jobskills/job_detail.html', context)


class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Jobs
    fields = ['title','type','req_skills','exp']
    template_name='jobskills/job_update.html'

    def form_valid(self,form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        job =self.get_object()
        if self.request.user == job.owner:
            return True
        else:
            return False


class JobDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
        model = Jobs
        success_url = 'owner-jobs'
        template_name = 'jobskills/jobs_confirm_delete.html'

        #test user to allow them to only update their own posts
        def test_func(self):
            job = self.get_object()
            if self.request.user == job.owner:
                return True
            else:
                return False
'''
class OwnerJobListView(LoginRequiredMixin, ListView):
    model = Jobs
    template_name = 'portal/owner_job.html'
    context_object_name = 'job'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Jobs.objects.filter(owner = user).order_by('-posted_date')
'''
@login_required
def ownerJobListView(request,pk):
    own = User.objects.get(pk=pk)
    job = Jobs.objects.filter(owner= own.id)

    page = request.GET.get('page',1)
    paginator = Paginator(job,6)
    try:
        job = paginator.page(page)
    except PageNotAnInteger:
        job = paginator.page(1)
    except EmptyPage:
        job = paginator.page(paginator.num_pages)

    for j in job:
        try:
            j.applied = AppliedJob.objects.filter(job_id = j.id).count()
            #print (AppliedJob.objects.filter(job_id = j.id).count())
        except:
            j.applied= 0


    context = {'job': job, 'own':own}

    return render(request,'jobskills/owner_job.html', context)

@login_required
def ownerJobDetailView(request,pk):
    job = Jobs.objects.get(pk=pk)

    '''Get Applied users'''
    aj = AppliedJob.objects.filter(job_id=pk)
    emp = []
    for j in aj:
        emp.append(str(j.applied_by))

    print(emp)

    sl = ShortList.objects.filter(job_id = pk)
    short_lst = []
    for s in sl:
        short_lst.append(s.emp_id)

    s_usr = User.objects.filter(pk__in = short_lst)
    usr = User.objects.filter(username__in = emp)

    context = {'job':job, 'usr':usr, 'sl':s_usr}

    return render(request, 'jobskills/owner_job_detail.html', context)


@login_required
def appliedProfile(request, empid, jobid):
    '''Profiles of applied candidates'''
    usr = User.objects.get(pk=empid)
    slisted = ShortList.objects.filter(job_id=jobid, emp_id=empid)
    context = {'usr':usr, 'slisted':slisted, 'jobid':jobid}


    if request.method == 'POST':
        emp_id = empid
        job_id = jobid
        ShortList.objects.create(emp_id = emp_id, job_id = job_id)

        usr = User.objects.get(pk=emp_id)
        job = Jobs.objects.get(pk=job_id)
        send_to = usr.email
        name = usr.username
        title = job.title
        skills = job.req_skills

        send_mail(send_to, name, title,skills)

        messages.success(request,f'Shortlisted successfully and user has been notified.')
        return redirect('owner-job-details', job_id)

    return render(request,'jobskills/applied_profile.html', context)

@login_required
def appliedJobs(request,pk):
    job1 = AppliedJob.objects.filter(applied_by = pk)
    j_lst = []
    for i in job1:
        j_lst.append(i.job_id)

    job = Jobs.objects.filter(id__in=j_lst).order_by('-posted_date')
    page = request.GET.get('page',1)
    paginator = Paginator(job,6)
    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        jobs = paginator.page(1)
    except EmptyPage:
        jobs = paginator.page(paginator.num_pages)


    return render(request, 'jobskills/applied_jobs.html', {'jobs':jobs})


##################################################################################
# Export data to files
##################################################################################
from django.http import HttpResponse
from users.models import Profile
def export_users_csv(request):
    '''export models to files'''
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['UserId', 'Primary_Skills', 'Secondary_skills', 'exp'])
    users = Profile.objects.all().values_list('user', 'p_skills', 's_skills', 'exp')
    for user in users:
        writer.writerow(user)

    return response

def export_job_csv2(request):
    '''export models to files'''
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="job.csv"'

    writer = csv.writer(response)
    writer.writerow(['JobId', 'title', 'req_skills', 'exp','type'])
    jobs = Jobs.objects.all().values_list('id', 'title', 'req_skills', 'exp', 'type')
    for job in jobs:
        writer.writerow(job)

    return response




#############################################################################################
#RECOMMENDER SYSTEM
#############################################################################################
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import linear_kernel,cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

@login_required
def recommend_jobs(request,pk):
    user1 = Profile.objects.filter(user=pk).values()
    #user = pd.Series(user)
    user = pd.DataFrame(user1,columns=['p_skills','s_skills','img','exp'])
    user['id'] = pk
    print (user.head())

    jobs = pd.DataFrame(list(Jobs.objects.exclude(owner=pk).values()),columns=['title','req_skills','exp'])
    jb = Jobs.objects.exclude(owner=pk)
    jid = []
    for j in jb:
        jid.append(j.id)
    jobs['id'] = jid
    #print (jobs.head())

    users_dta = user['p_skills']+' '+user['s_skills']
    jobs_dta = jobs['title']+' '+jobs['req_skills']

    jobid = jobs['id']

    data1 = pd.concat([users_dta,jobs_dta]).reset_index(drop=True)

    count = CountVectorizer(stop_words='english', ngram_range=(1, 2))
    mat = count.fit_transform(data1)
    score = linear_kernel(mat,mat)
    req_score = score[0]
    req1_score = list(enumerate(req_score))
    req1_score = req1_score[1:]
    req1_score = pd.DataFrame(req1_score,columns=['index','score'])
    req1_score['JobId'] = jobid
    req1_score = req1_score.sort_values(by='score', ascending=False)
    req1_score = req1_score[req1_score['score']>=1]['JobId']

    recomm_jobs = Jobs.objects.filter(id__in=req1_score)
    page = request.GET.get('page',1)

    paginator = Paginator(recomm_jobs,6)

    try:
        recomm_jobs = paginator.page(page)
    except PageNotAnInteger:
        recomm_jobs = paginator.page(1)
    except EmptyPage:
        recomm_jobs = paginator.page(paginator.num_pages)

    for j in recomm_jobs:
        print(j.id)
    context = {'jobs':recomm_jobs}

    return render(request,'jobskills/recommend_job.html', context)


def recommend_search(request):
    if request.method == 'POST':
        form = searchForm(request.POST)
        if form.is_valid():
            skills = form.cleaned_data.get('Skills')
            exp = form.cleaned_data.get('Experience')
            type = form.cleaned_data.get('Type')

            jobs = pd.DataFrame(list(Jobs.objects.filter(exp__gte=exp, type= type).values()),columns=['id','title','req_skills','exp'])

            jobs_data = jobs['title'] + jobs['req_skills']

            search_data = pd.Series(skills)
            data1 = pd.concat([search_data, jobs_data]).reset_index(drop=True)

            count = CountVectorizer(stop_words='english')
            mat = count.fit_transform(data1)
            score = linear_kernel(mat,mat)
            req_score = score[0]
            req1_score = list(enumerate(req_score))
            req1_score = req1_score[1:]
            req1_score = pd.DataFrame(req1_score,columns=['index','score'])
            req1_score['JobId'] = jobs['id']

            req1_score = req1_score.sort_values(by='score', ascending=False)

            req1_score = req1_score[req1_score['score']>=1]['JobId']

            recomm_jobs = Jobs.objects.filter(id__in=req1_score).order_by('-posted_date')

            context ={'form':form,'jobs':recomm_jobs}


            return render(request,'jobskills/search_jobs.html', context)
    else:
        form = searchForm()
        print ('Iam here')
        context ={'form':form}
        return render(request,'jobskills/search_jobs.html', context)
