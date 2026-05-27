from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Job, JobDetails
from student.models import StudentProfile
from employer.models import Employer
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        if StudentProfile.objects.filter(student=request.user).exists():
            return redirect('home')
        else:
            return redirect('ehome')
    query = request.GET.get('q')
    location = request.GET.get('location')
    company = request.GET.get('company')

    jobs = Job.objects.all().order_by('-created_at')

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    if location:
        jobs = jobs.filter(location__icontains=location)

    if company:
        jobs = jobs.filter(company__icontains=company)

    locations = Job.objects.values_list('location',flat=True).distinct()
    companies = Job.objects.values_list('company',flat=True).distinct()

    paginator = Paginator(jobs, 2)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'jobs': jobs,
        'locations': locations,
        'companies': companies,
        'page_obj': page_obj,
    }



    return render(request, 'home.html', context)

def latest_job(request):
    msg = False
    if request.user.is_authenticated:
        if Employer.objects.filter(user=request.user).exists():
            msg = True
    all_job = Job.objects.all()
    d = {'jobs':all_job,'msg':msg}
    return render(request, 'latest_job.html', d)

def job_details(request,id):
    msg = False

    if request.user.is_authenticated:
        if Employer.objects.filter(user=request.user).exists():
            msg = True

    job = Job.objects.get(id = id)
    try:
        jobdetails = JobDetails.objects.get(job=job)
    except JobDetails.DoesNotExist:
        jobdetails = None
    d = {'jobdetails':jobdetails,'msg':msg}
    return render(request, 'job_details.html', d)

