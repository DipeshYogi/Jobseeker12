from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('alljobs/', views.allJobs, name='all-jobs'),
    path('job/new/', views.JobCreateView.as_view(), name='create-job'),
    path('job/<int:pk>/', views.jobdetailview, name='job-detail'),
    path('job/<int:pk>/update/', views.JobUpdateView.as_view(), name='job-update'),
    path('job/<int:pk>/delete/', views.JobDeleteView.as_view(), name='job-delete'),
    path('user/<int:pk>/', views.ownerJobListView,name='owner-jobs'),
    path('user/<int:pk>/details/', views.ownerJobDetailView, name='owner-job-details'),
    path('application/<int:empid>/<int:jobid>/profile', views.appliedProfile, name = 'applied-profile' ),
    path('exp/', views.export_users_csv, name = 'exp-data'),
    path('exp2/', views.export_job_csv2, name = 'exp-data2'),
    path('user/<int:pk>/recommended/', views.recommend_jobs, name='recommend-job'),
    path('search/', views.recommend_search, name = 'job-search'),
    path('applied-jobs/<int:pk>/', views.appliedJobs, name='applied-jobs'),


]
