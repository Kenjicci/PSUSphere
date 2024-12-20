from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    upated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class College(BaseModel):
    college_name = models.CharField (max_length=150)

    def __str__(self):
        return self.college_name
    
class Program(BaseModel):
    prog_name = models.CharField (max_length=150)
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self):
        return self.prog_name
    
class Organization(BaseModel):
    name = models.CharField(max_length=250, verbose_name="Organization Name")
    college = models.ForeignKey(
        College, null=True, blank=True, on_delete=models.CASCADE, verbose_name="College")
    description = models.CharField(max_length=500)
    
    def __str__(self):
        return self.name
    
class Student(BaseModel):
    student_id = models.CharField(max_length=15)
    lastname = models.CharField(max_length=25, verbose_name="Last Name")
    firstname = models.CharField(max_length=25, verbose_name="First Name")
    middlename = models.CharField(max_length=25, blank=True, null=True, verbose_name="Middle Name")
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.lastname}, {self.firstname}"
    
    
class OrgMember(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Student")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="Organization")
    date_joined = models.DateField()

    def __str__(self):
        return f"{self.student}"
