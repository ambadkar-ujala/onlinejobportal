from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import StudentProfile, Education, Experience
from employer.models import Employer
from job.models import Job, Application,SavedJob
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
import re
from django.core.mail import send_mail

# Create your views here.

def register1(request):
    if request.method == 'POST':
            uname = request.POST['username']
            pname = request.POST['password']
            cpass = request.POST['confirmpassword']

            pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$'

            if pname != cpass:
                messages.error(request, 'Passwords do not match')

            elif not re.match(pattern, pname):
                messages.error(request,
                    'Password must contain uppercase, lowercase, number, special character and minimum 8 characters'
                )

            else:
                User.objects.create_user(username=uname,password=pname)
                messages.success(request, 'Registration Successful')
            return redirect('login1')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

def login1(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)



            if Employer.objects.filter(user=request.user).exists():
                return redirect('ehome')
            else:
                return redirect('home')
        else:
            messages.error(request, "Incorrect Username or Password")

    else:
        form = AuthenticationForm(request)

    return render(request, 'login.html', {'form': form})


def logout1(request):
    logout(request)
    return redirect('login1')

@login_required
def change_password(request):
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
    return render(request, 'change_password.html', d)


def student_profile(request):
    d = {}
    if request.user.is_authenticated:

            if request.method == 'POST':
                firstname = request.POST['firstname']
                lastname = request.POST['lastname']
                email_id = request.POST['email_id']
                contact = request.POST['contact']
                gender = request.POST['gender']
                location = request.POST['location']
                image = request.FILES.get('image')
                skills = request.POST['skills']
                resume = request.FILES.get('resume')
                language = request.POST.getlist('language')
                language = ", ".join(language)
                student = request.user
                pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                pattern1 = r"^(\+91)?[6-9]\d{9}$"
                if  re.fullmatch(pattern, email_id) and re.match(pattern1,contact):
                    StudentProfile.objects.create(student=student,
                                              firstname=firstname,
                                              lastname=lastname,
                                              email_id=email_id,
                                              contact=contact,
                                              image=image,
                                              gender=gender,
                                              skills=skills,
                                              resume=resume,
                                              location=location,
                                              language=language
                                              )
                else:
                    messages.error(request, 'Email or Contact No. is not valid!')
                    d = {'messages':messages}
                return redirect('student_details')

    return render(request,'student_profile.html', d)

@login_required
def update_student(request,id):
    stud = StudentProfile.objects.get(id=id)
    educations = Education.objects.filter(studuser=stud)
    experiences = Experience.objects.filter(stud=stud)
    if stud:
        if request.method == 'POST':
            if request.POST.get('firstname'):
                stud.firstname = request.POST.get('firstname')
            if  request.POST.get('lastname'):
                stud.lastname = request.POST.get('lastname')
            if request.POST.get('email_id'):
                stud.email_id = request.POST.get('email_id')
            if request.POST.get('contact'):
                stud.contact = request.POST.get('contact')
            if request.POST.get('gender'):
                stud.gender = request.POST.get('gender')
            if request.POST.get('skills'):
                stud.skills = request.POST.get('skills')
            if request.POST.get('location'):
                stud.location = request.POST.get('location')
            if request.POST.getlist('language'):
                stud.language = request.POST.getlist('language')
                stud.language = ", ".join(stud.language)

            if 'image' in request.FILES:
                stud.image = request.FILES['image']


            if 'resume' in request.FILES:
                stud.resume = request.FILES['resume']


            stud.save()

            return redirect('student_details')

    return render(request, 'update_student.html', {'stud': stud,'educations':educations,'experiences':experiences })

def delete_profile(request, id):
    if request.user.is_authenticated == True:
        user = User.objects.get(id=id)
        user.delete()
    return redirect('logout1')



@login_required
def student_details(request):
    error = ''
    student = StudentProfile.objects.filter(student=request.user).first()
    educations = Education.objects.filter(studuser=student)
    experiences = Experience.objects.filter(stud=student)
    total_experience = 0
    for exp in experiences:
        experience = exp.enddate - exp.startdate
        total_exp = total_experience + experience.days

    years = total_exp // 365

    months = (total_exp % 365) // 30

    total_experience = f"{years} Years {months} Months"

    if student:
        error = 'yes'
        d = {'student':student,'educations':educations,'experiences':experiences, 'error':error, 'total_experience':total_experience}

    else:
        messages.error(request, "Profile not available. Please create your profile first!")
        d = {}
        return redirect('student_profile')


    return render(request, 'student_details.html', d)

def save_job(request, id):
    if request.user.is_authenticated:
        job = Job.objects.get(id=id)
        student = StudentProfile.objects.get(student=request.user)
        SavedJob.objects.create(student=student, job=job)
        return redirect('home')
    return render(request, 'home.html')

def unsave_job(request,id):
    student = StudentProfile.objects.get(student=request.user)
    saved_job = SavedJob.objects.get(id=id)
    saved_job.delete()
    return redirect('home')

@login_required
def saved_job(request):
    student = StudentProfile.objects.get(student=request.user)
    saved_job = SavedJob.objects.filter(student=student)

    for i in saved_job:
        job = Job.objects.get(id=i.job.id)
        already_applied = Application.objects.filter(student=student, job=job).exists()
        if already_applied:
            SavedJob.objects.filter(
                student=student,
                job=job
            ).delete()

    d = {'saved_job':saved_job}
    return render(request, 'saved_job.html',d )

@login_required
def applied_job(request):
    student = StudentProfile.objects.get(student=request.user)
    applied_job = Application.objects.filter(student=student)
    d = {'applied_job':applied_job}
    return render(request, 'applied_job.html',d )


@login_required
def apply_job(request,id):
        job = Job.objects.get(id=id)
        student = StudentProfile.objects.get(student=request.user)
        already_applied = Application.objects.filter(student=student, job=job).exists()

        if already_applied:
            return redirect('home')

        if request.method == 'POST':
            resume = request.FILES.get('resume')
            try:
                student = StudentProfile.objects.get(student=request.user)
            except StudentProfile.DoesNotExist:
                return HttpResponse("Employer profile not found")
            Application.objects.create(
                student=student,
                job=job,
                resume=resume
            )
            send_mail(
                subject="Job Appication",
                message="You have applied to the job successfully",
                from_email="ujala.ikhar@gmail.com",
                recipient_list=[student.email_id]
            )
            return redirect('home')

        return render(request, 'apply.html', {'job': job})

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        send_mail(
            subject="Password Reset",
            message='http://127.0.0.1:8000/password_reset/',
            from_email="ujala.ikhar@gmail.com",
            recipient_list=[email]
        )
        return redirect('home')
    return render(request, 'forgot_password.html')


def password_reset(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        password1 = request.POST['cpass']
        user = User.objects.filter(username=username).first()

        if user:
            if password == password1:
                user.set_password(password)
                user.save()
                messages.success(request, 'Password is changed successfully')
                return redirect('login1')
            else:
                messages.error(request, 'New password and confirm password are not same!')

        else:
            messages.error(request, 'User not available!')

    return render(request,'password_reset.html')

@login_required()
def student_education(request):
    student = StudentProfile.objects.get(student=request.user)

    if student:
        if request.method == 'POST':
            education_type = request.POST['education_type']
            degree = request.POST['degree']
            school_college= request.POST['school_college']
            board_university = request.POST['board_university']
            specialization = request.POST['specialization']
            passing_year = request.POST['passing_year']
            marks = request.POST['marks']
            Education.objects.create(studuser=student,education_type=education_type,degree=degree,school_college=school_college,
                                 board_university=board_university,specialization=specialization,
                                 passing_year=passing_year,marks=marks)

            return redirect('student_details')

    return render(request,'student_education.html')


@login_required
def student_experience(request):
    student = StudentProfile.objects.get(student=request.user)
    if student:
        if request.method == 'POST':
            job_title = request.POST['job_title']
            company_name = request.POST['company_name']
            startdate = request.POST['startdate']
            enddate = request.POST['enddate']
            salary = request.POST['salary']
            job_profile = request.POST['job_profile']
            Experience.objects.create(stud=student,job_title=job_title,company_name=company_name,
                                      startdate=startdate,enddate=enddate,salary=salary,job_profile=job_profile)
            return redirect('student_details')
    return render(request,'student_experience.html')

@login_required
def edit_education(request):
    student = StudentProfile.objects.get(student=request.user)
    educations = Education.objects.filter(studuser=student)
    if request.method == 'POST':
            for education in educations:
                if education.education_type == '10th':
                    education.school_college = request.POST.get('school_college')
                    education.board_university = request.POST.get('board_university')
                    education.passing_year = request.POST.get('passing_year')
                    education.marks = request.POST.get('marks')
                    education.save()
                    return redirect('student_details')
    return render(request, 'edit_education.html', {'educations': educations})

@login_required
def edit_education12(request):
    student = StudentProfile.objects.get(student=request.user)
    educations = Education.objects.filter(studuser=student)
    if request.method == 'POST':

            for education in educations:
                if education.education_type == '12th':
                    education.school_college = request.POST.get('school_college')
                    education.board_university = request.POST.get('board_university')
                    education.passing_year = request.POST.get('passing_year')
                    education.marks = request.POST.get('marks')
                    education.save()
                    return redirect('student_details')
    return render(request, 'edit_12.html', {'educations': educations})

@login_required
def edit_educationgr(request):
    student = StudentProfile.objects.get(student=request.user)
    educations = Education.objects.filter(studuser=student)
    if request.method == 'POST':
        for education in educations:
            if education.education_type == 'Graduation':
                education.degree = request.POST.get('degree')
                education.school_college = request.POST.get('school_college')
                education.board_university = request.POST.get('board_university')
                education.specialization = request.POST.get('specialization')
                education.passing_year = request.POST.get('passing_year')
                education.marks = request.POST.get('marks')
                education.save()
                return redirect('student_details')
    return render(request, 'edit_grad.html', {'educations': educations})

@login_required
def edit_educationpg(request):
    student = StudentProfile.objects.get(student=request.user)
    educations = Education.objects.filter(studuser=student)
    if request.method == 'POST':
        for education in educations:
            if education.education_type == 'Post Graduation':
                education.degree = request.POST.get('degree')
                education.school_college = request.POST.get('school_college')
                education.board_university = request.POST.get('board_university')
                education.specialization = request.POST.get('specialization')
                education.passing_year = request.POST.get('passing_year')
                education.marks = request.POST.get('marks')
                education.save()
                return redirect('student_details')
    return render(request, 'edit_pg.html', {'educations': educations})

def edit_experience(request):
    student = StudentProfile.objects.get(student=request.user)
    experiences = Experience.objects.filter(stud=student)
    for experience in experiences:
        if request.method == 'POST':
            experience.job_title = request.POST.get('job_title')
            experience.company_name = request.POST.get('company_name')
            experience.startdate = request.POST.get('startdate')
            experience.enddate = request.POST.get('enddate')
            experience.salary = request.POST.get('salary')
            experience.job_profile = request.POST.get('job_profile')
            experience.save()
            return redirect('student_details')
    return render(request, 'edit_exp.html', {'experiences':experiences})

def change_image(request):
    student = StudentProfile.objects.get(student=request.user)
    if request.method == 'POST':
        student.image = request.FILES.get('image')
        student.save()
        return redirect('student_details')
    return render(request, 'change_image.html')

def update_resume(request):
    student = StudentProfile.objects.get(student=request.user)
    if request.method == 'POST':
        student.resume = request.FILES.get('resume')
        student.save()
        return redirect('student_details')
    return render(request, 'update_resume.html')

def delete_education(request, id):
    education = Education.objects.get(id=id)
    education.delete()
    return redirect('student_details')

def delete_experience(request):
    experience = Experience.objects.get(id=id)
    experience.delete()
    return redirect('student_details')


