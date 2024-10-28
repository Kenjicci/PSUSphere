from django.contrib import admin

from .models import College, Program, Organization, Student, OrgMember

admin.site.register(College)
@admin.register(Program)
class Program(admin.ModelAdmin):
    list_display = ("prog_name", "college")
    search_fields = ("prog_name", "colege")

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "college")
    search_fields = ("name", "college")


@admin.register(Student) 
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "lastname",
                    "firstname", "middlename", "program", "get_college_name")
    search_fields = ("lastname", "firstname",)
    
    @admin.display(description="College")
    def get_college_name(self, obj):
            return obj.program.college.college_name
    

@admin.register(OrgMember)
class OrgMemberAdmin(admin.ModelAdmin):
    list_display = ("student", "get_member_program", "get_college_name", "organization",
                    "date_joined",)
    search_fields = ("student__lastname", "student__firstname",)
    
    @admin.display(description="Program")
    def get_member_program(self, obj):
        try:
            member = Student.objects.get(id=obj.student_id)
            return member.program 
        except Student.DoesNotExist:
            return None 
        
    @admin.display(description="College")
    def get_college_name(self, obj):
            return obj.student.program.college.college_name
        