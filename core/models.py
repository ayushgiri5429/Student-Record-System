from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class College(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10, unique=True)
    address = models.TextField()
    established_date = models.DateField()
    is_autonomous = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Course(models.Model):
    COURSE_TYPES = (
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
        ('DP', 'Diploma'),
        ('CR', 'Certificate'),
    )
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10, unique=True)
    duration = models.IntegerField(help_text="Duration in years")
    course_type = models.CharField(max_length=2, choices=COURSE_TYPES)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='courses')
    
    def __str__(self):
        return f"{self.name} - {self.college.name}"

class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Admission(models.Model):
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
        ('C', 'Cancelled'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='admissions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='admissions')
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='admissions')
    admission_date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    remarks = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('student', 'course', 'college')
    
    def __str__(self):
        return f"{self.student} - {self.course} ({self.get_status_display()})"
    

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('viewer', 'Viewer'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='viewer')

    def __str__(self):
        return f'{self.user.username} - {self.role}'
