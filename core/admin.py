from django.contrib import admin
from .models import Student, Course, College, Admission, UserProfile

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'email', 'phone', 'created_at')
    list_filter = ('gender', 'created_at')
    search_fields = ('student_id', 'first_name', 'last_name', 'email')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'course_type', 'duration', 'fees', 'college')
    list_filter = ('course_type', 'college')
    search_fields = ('name', 'code')

@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'established_date', 'is_autonomous')
    list_filter = ('is_autonomous', 'established_date')
    search_fields = ('name', 'code')

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'college', 'admission_date', 'status')
    list_filter = ('status', 'admission_date', 'college')
    search_fields = ('student__first_name', 'student__last_name', 'course__name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_editable = ('role',)  # Allow changing role directly in the list
    search_fields = ('user__username', 'role')