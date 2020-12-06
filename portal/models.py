from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Jobs(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, verbose_name='Job Title')

    Choices = (
                ('Full time','Full time'),
                ('Part time','Part time'),
                ('Contract based','Contract based'),
    )
    type = models.CharField(max_length=20,verbose_name='Job type',choices = Choices)
    req_skills = models.TextField(verbose_name='Required Skills')
    exp = models.PositiveIntegerField(verbose_name=f'Experience (in years)')
    posted_date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('job-detail', kwargs={'pk':self.pk})


    class Meta:
       verbose_name_plural = "Jobs"



class AppliedJob(models.Model):
        applied_by = models.ForeignKey(User, on_delete=models.CASCADE)
        job_id = models.IntegerField(null=True)

        def __str__(self):
            return str(self.applied_by)+'_'+str(self.job_id)

        def get_absolute_url(self):
            return reverse('job-detail', kwargs={'pk':self.pk})


class ShortList(models.Model):
    job_id = models.IntegerField()
    emp_id = models.IntegerField()

    def __str__(self):
        return str(self.job_id)+'_'+str(self.emp_id)

    def get_absolute_url(self):
        return reverse('owner-job-details', kwargs={'pk':self.pk})
