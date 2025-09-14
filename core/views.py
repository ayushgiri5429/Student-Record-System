from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Student, Course, College, Admission, UserProfile
from .forms import (
    UserRegistrationForm, StudentForm, CourseForm, 
    CollegeForm, AdmissionForm, SearchForm
)
from .decorators import viewer_required, editor_required, admin_required

# ---------------- User Registration ----------------
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile with default 'viewer' role
            UserProfile.objects.create(user=user, role='viewer')
            login(request, user)
            messages.success(request, 'Registration successful! You have been granted viewer access.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/register.html', {'form': form})

# ---------------- Login / Logout ----------------
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'core/login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

# ---------------- Home Page ----------------
@viewer_required
def home(request):
    student_count = Student.objects.count()
    course_count = Course.objects.count()
    college_count = College.objects.count()
    admission_count = Admission.objects.count()
    
    recent_admissions = Admission.objects.select_related('student', 'course', 'college').order_by('-created_at')[:5]
    
    recent_activities = []
    for admission in recent_admissions:
        recent_activities.append({
            'title': f'New Admission - {admission.student.first_name} {admission.student.last_name}',
            'description': f'Admitted to {admission.course.name} at {admission.college.name}',
            'time': admission.created_at.strftime('%b %d, %Y at %H:%M'),
            'status': admission.get_status_display(),
            'type': 'admission'
        })
    
    if not recent_activities:
        recent_activities = [
            {
                'title': 'System Initialized',
                'description': 'Student Record System is now ready for use',
                'time': 'Just now',
                'type': 'system'
            },
            {
                'title': 'Welcome!',
                'description': 'Start by adding colleges, courses, and students',
                'time': 'Today',
                'type': 'info'
            }
        ]
    
    context = {
        'student_count': student_count,
        'course_count': course_count,
        'college_count': college_count,
        'admission_count': admission_count,
        'recent_activities': recent_activities
    }
    return render(request, 'core/home.html', context)

# ---------------- List Views ----------------
@viewer_required
def student_list(request):
    form = SearchForm(request.GET or None)
    students = Student.objects.all()
    query = request.GET.get('query')
    if query:
        students = students.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(student_id__icontains=query) |
            Q(email__icontains=query)
        )
    context = {'students': students, 'form': form, 'search_query': query}
    return render(request, 'core/student_list.html', context)

@viewer_required
def course_list(request):
    form = SearchForm(request.GET or None)
    courses = Course.objects.all()
    query = request.GET.get('query')
    if query:
        courses = courses.filter(
            Q(name__icontains=query) |
            Q(code__icontains=query) |
            Q(college__name__icontains=query)
        )
    context = {'courses': courses, 'form': form, 'search_query': query}
    return render(request, 'core/course_list.html', context)

@viewer_required
def college_list(request):
    form = SearchForm(request.GET or None)
    colleges = College.objects.all()
    query = request.GET.get('query')
    if query:
        colleges = colleges.filter(
            Q(name__icontains=query) |
            Q(code__icontains=query) |
            Q(address__icontains=query)
        )
    context = {'colleges': colleges, 'form': form, 'search_query': query}
    return render(request, 'core/college_list.html', context)

@viewer_required
def admission_list(request):
    form = SearchForm(request.GET or None)
    admissions = Admission.objects.all()
    query = request.GET.get('query')
    if query:
        admissions = admissions.filter(
            Q(student__first_name__icontains=query) |
            Q(student__last_name__icontains=query) |
            Q(course__name__icontains=query) |
            Q(college__name__icontains=query)
        )
    context = {'admissions': admissions, 'form': form, 'search_query': query}
    return render(request, 'core/admission_list.html', context)

# ---------------- Add / Create Views ----------------
@editor_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES or None)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student {student.full_name} added successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'core/student_form.html', {'form': form, 'title': 'Add Student'})

@editor_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, f'Course {course.name} added successfully!')
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'core/course_form.html', {'form': form, 'title': 'Add Course'})

@editor_required
def add_college(request):
    if request.method == 'POST':
        form = CollegeForm(request.POST)
        if form.is_valid():
            college = form.save()
            messages.success(request, f'College {college.name} added successfully!')
            return redirect('college_list')
    else:
        form = CollegeForm()
    return render(request, 'core/college_form.html', {'form': form, 'title': 'Add College'})

@editor_required
def add_admission(request):
    if request.method == 'POST':
        form = AdmissionForm(request.POST)
        if form.is_valid():
            admission = form.save(commit=False)
            admission.created_by = request.user
            admission.save()
            messages.success(request, f'Admission for {admission.student} added successfully!')
            return redirect('admission_list')
    else:
        form = AdmissionForm()
    return render(request, 'core/admission_form.html', {'form': form, 'title': 'Add Admission'})

# ---------------- Edit Views ----------------
@editor_required
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES or None, instance=student)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student {student.full_name} updated successfully!')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'core/student_form.html', {'form': form, 'title': 'Edit Student'})

@editor_required
def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save()
            messages.success(request, f'Course {course.name} updated successfully!')
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'core/course_form.html', {'form': form, 'title': 'Edit Course'})

@editor_required
def edit_college(request, pk):
    college = get_object_or_404(College, pk=pk)
    if request.method == 'POST':
        form = CollegeForm(request.POST, instance=college)
        if form.is_valid():
            college = form.save()
            messages.success(request, f'College {college.name} updated successfully!')
            return redirect('college_list')
    else:
        form = CollegeForm(instance=college)
    return render(request, 'core/college_form.html', {'form': form, 'title': 'Edit College'})

@editor_required
def edit_admission(request, pk):
    admission = get_object_or_404(Admission, pk=pk)
    if request.method == 'POST':
        form = AdmissionForm(request.POST, instance=admission)
        if form.is_valid():
            admission = form.save()
            messages.success(request, f'Admission for {admission.student} updated successfully!')
            return redirect('admission_list')
    else:
        form = AdmissionForm(instance=admission)
    return render(request, 'core/admission_form.html', {'form': form, 'title': 'Edit Admission'})

# ---------------- Delete Views ----------------
@admin_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, f'Student {student.full_name} deleted successfully!')
        return redirect('student_list')
    return render(request, 'core/student_confirm_delete.html', {'student': student})

@admin_required
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, f'Course {course.name} deleted successfully!')
        return redirect('course_list')
    return render(request, 'core/course_confirm_delete.html', {'course': course})

@admin_required
def delete_college(request, pk):
    college = get_object_or_404(College, pk=pk)
    if request.method == 'POST':
        college.delete()
        messages.success(request, f'College {college.name} deleted successfully!')
        return redirect('college_list')
    return render(request, 'core/college_confirm_delete.html', {'college': college})

@admin_required
def delete_admission(request, pk):
    admission = get_object_or_404(Admission, pk=pk)
    if request.method == 'POST':
        admission.delete()
        messages.success(request, f'Admission for {admission.student} deleted successfully!')
        return redirect('admission_list')
    return render(request, 'core/admission_confirm_delete.html', {'admission': admission})
