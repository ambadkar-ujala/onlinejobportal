from django.shortcuts import render, redirect, HttpResponse
from .models import Employer
from student.models import StudentProfile
from job.models import Job, Application, JobDetails
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
import re
# Create your views here.


def ehome(request):
    if request.user.is_authenticated:
        employer = Employer.objects.get(user=request.user)
        d = {'employer':employer}

    else:
        d = {}
    return render(request, 'ehome.html', d )

def register2(request):
    if request.method == 'POST':
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        email = request.POST['email_id']
        company = request.POST['company']
        contact = request.POST['contact']
        image = request.FILES.get('image')
        gender = request.POST['gender']
        uname = request.POST['username']
        pname = request.POST['password']
        cpass = request.POST['confirmpassword']

        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$'
        if re.match(pattern, pname):
            if (pname == cpass):
                user = User.objects.create_user(username=uname, password=pname)
            else:
                messages.error(request, 'Passwords do not match')
        else:
            messages.error(request, 'Password must contain uppercase, lowercase, number, special character and minimum 8 characters')

        pattern1 = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        pattern2 = r"^(\+91)?[6-9]\d{9}$"
        if re.fullmatch(pattern1, email) and re.match(pattern2, contact):
            Employer.objects.create(user=user,firstname=fname,lastname=lname,email_id=email,company=company,contact=contact,image=image,gender=gender)
            return redirect('home')
        else:
            messages.error(request,'Email or Contact No. is not valid!')
    else:
        form = UserCreationForm()

    return render(request, 'eregister.html', {'form': form})

def login2(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if StudentProfile.objects.filter(student=request.user).exists():
                return redirect('home')
            else:
                return redirect('ehome')
        else:
            messages.error(request, "Incorrect Username or Password")
    else:
        form = AuthenticationForm(request)

    return render(request, 'elogin.html', {'form': form})


def logout2(request):
    logout(request)
    return redirect('login2')

@login_required
def change_emppassword(request):
    error = " "
    if request.method == 'POST':
        oldp = request.POST['oldp']
        newp = request.POST['newp']
        conp = request.POST['conp']
        user  =  User.objects.get(id=request.user.id)
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$'
        if user.check_password(oldp):
            if re.match(pattern,newp):
                if newp == conp:
                    user.set_password(newp)
                    user.save()
                    return redirect('logout1')
                else:
                    error = 'New password and confirm password are not same'
            else:
                error = 'Password must contain uppercase, lowercase, number, special character and minimum 8 characters'
        else:
            error = 'Old Password is incorrect!'

    d = {'error':error}
    return render(request, 'change_emppassword.html', d)




def update_employer(request):
    employer = Employer.objects.get(user=request.user)
    if request.user.is_authenticated:

        if request.method == 'POST':
            employer.firstname = request.POST['firstname']
            employer.lastname = request.POST['lastname']
            employer.email_id = request.POST['email_id']
            employer.company = request.POST['company']
            employer.contact = request.POST['contact']
            employer.image = request.FILES.get('image')
            employer.gender = request.POST['gender']
            employer.save()


    return render(request, 'update_employer.html', {'employer':employer})

def employer_profile(request):
    if request.user.is_authenticated == True:
        employer = Employer.objects.get(user=request.user)
    return render(request, 'ehome.html', {'employer':employer})

def delete_profile(request, id):
    if request.user.is_authenticated == True:
        user = User.objects.get(id=id)
        user.delete()
    return redirect('logout1')




@login_required
def post_job(request):
    if request.method == 'POST':
        title = request.POST['title']
        location = request.POST['location']
        startdate = request.POST['startdate']
        enddate = request.POST['enddate']
        description = request.POST['description']
        company = request.POST['company']
        com_logo = request.FILES.get('com_logo')
        experience = request.POST['experience']
        skills = request.POST['skills']
        salary = request.POST['salary']
        job_requirements = request.POST['req']
        job_responsibilities = request.POST['res']
        no_of_employees = request.POST['no_of_employees']
        registration_no = request.POST['reg']
        company_info = request.POST['info']
        company_address = request.POST['address']
        try:
            employer = Employer.objects.get(user=request.user)
        except Employer.DoesNotExist:
            return HttpResponse("Employer profile not found")
        job = Job.objects.create(employer=employer,start_date=startdate,end_date=enddate,title=title,company=company,location=location,
                           description=description,experience=experience,skills=skills,salary=salary,company_logo=com_logo)
        JobDetails.objects.create(job=job,job_requirements=job_requirements,job_responsibilities = job_responsibilities,
                                  no_of_employees = no_of_employees,registration_no = registration_no,company_info = company_info,
                                  company_address = company_address)
        return redirect('ehome')
    return render(request, 'post_job.html')

@login_required
def edit_job(request,id):
    employer = Employer.objects.get(user=request.user)
    job = Job.objects.get(id=id)
    jobdetails = JobDetails.objects.get(job=job)
    if request.method == 'POST':
        job.title = request.POST['title']
        job.location = request.POST['location']
        job.star_tdate = request.POST['startdate']
        job.end_date = request.POST['enddate']
        job.description = request.POST['description']
        job.company = request.POST['company']
        job.experience = request.POST['experience']
        job.skills = request.POST['skills']
        job.salary = request.POST['salary']
        job.save()
        jobdetails.job_requirements = request.POST['req']
        jobdetails.job_responsibilities = request.POST['res']
        jobdetails.no_of_employees = request.POST['no_of_employees']
        jobdetails.registration_no = request.POST['reg']
        jobdetails.company_info = request.POST['info']
        jobdetails.company_address = request.POST['address']
        jobdetails.save()
        return redirect('job_list')
    d = {'job':job,'jobdetails':jobdetails }
    return render(request, 'edit_job.html', d)

def delete_job(request,id):
    job = Job.objects.get(id=id)
    job.delete()
    return redirect('job_list')

def job_list(request):
    if request.user.is_authenticated:
        employer = Employer.objects.get(user=request.user)
        job_list = Job.objects.filter(employer=employer)
        d = {'job_list':job_list}
    return render(request, 'job_list.html', d)

def candidate_applied(request):
    app_obj = []
    if request.user.is_authenticated:
        employer = Employer.objects.get(user=request.user)
        job_list = Job.objects.filter(employer=employer)
        for job in job_list:
            apps = Application.objects.filter(job=job)
            for app in apps:
                app_obj.append(app)
        d = {'app_obj': app_obj}
    return render(request, 'candidate_applied.html', d)

