from django.conf import settings
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    register_number = models.CharField(max_length=12, primary_key=True, null=False)
    password = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    last_activity = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.register_number}"

class LoginAuthentication(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.student.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    credit_hours = models.IntegerField()
    faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField()

    def __str__(self):
        return f"{self.student} - {self.course}"


class Faculty(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)
    department_head = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Degree(models.Model):
    name = models.CharField(max_length=100)
    degree_code = models.CharField(max_length=10)
    required_courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.name


class Transcript(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.student} - {self.course}"


class ClassSection(models.Model):
    section_name = models.CharField(max_length=10)
    students = models.ManyToManyField(Student, related_name='class_sections')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.section_name} ({self.start_time} - {self.end_time}, {self.day}, Faculty: {self.faculty}, Students: {', '.join(str(s) for s in self.students.all())})"

