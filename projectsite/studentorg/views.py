from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.models import Organization, OrgMember, Student, College, Program
from studentorg.forms import OrganizationForm, OrgMemberForm, StudentForm, CollegeForm, ProgramForm
from django.urls import reverse_lazy
from typing import Any
from django.db.models.query import QuerySet
from django.db.models.query import Q
from django.utils.decorators import method_decorator 
from django.contrib.auth.decorators import login_required 
from django.db import connection
from django.http import JsonResponse
from django.contrib import messages

@method_decorator(login_required, name="dispatch")
class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"

class ChartView(ListView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        pass

#ORGANIZATIONS
class OrganizationList(ListView):
     model = Organization 
     context_object_name = 'organization' 
     template_name = 'org_list.html' 
     paginate_by = 5 
     
     def get_queryset(self, *args, **kwargs):
         qs = super(OrganizationList, self).get_queryset(*args, **kwargs)
         if self.request.GET.get("q") != None: 
             query = self.request.GET.get('q') 
             qs = qs.filter(Q(name__icontains=query) | 
                            Q(college__college_name__icontains=query) |
                            Q(description__icontains=query)) 
         return qs 

class OrganizationCreateView(CreateView):
     model = Organization
     form_class = OrganizationForm
     template_name = 'org_add.html'
     success_url = reverse_lazy('organization-list')

     def form_valid(self, form):
          org_name = form.instance.name
          messages.success(self.request, f'{org_name} has been successfully added.')

          return super().form_valid(form)


class OrganizationUpdateView(UpdateView):
     model = Organization
     form_class = OrganizationForm
     template_name = 'org_edit.html'
     success_url = reverse_lazy('organization-list')

     def form_valid(self, form):
          org_name = form.instance.name
          messages.success(self.request, f'{org_name} has been successfully updated.')

          return super().form_valid(form)
     
class OrganizationDeleteView(DeleteView):
     model = Organization
     # form_class = OrganizationForm
     template_name = 'org_del.html'
     success_url = reverse_lazy('organization-list')

     ''''#not working
     def form_valid(self, form):
          org_name = form.instance.name
          messages.success(self.request, f'{org_name} has been successfully deleted.')

          return super().form_valid(form)
     '''

#ORGMEMBERS 
class OrgMemberList(ListView):
     model = OrgMember
     context_object_name = 'orgmember'
     template_name = 'orgmember_list.html'
     paginate_by = 5
        
     def get_queryset(self, *args, **kwargs):
          qs = super(OrgMemberList, self).get_queryset(*args, **kwargs)
          if self.request.GET.get("q") !=None:
               query = self.request.GET.get('q')
               qs = qs.filter(Q(student__firstname__icontains=query) | 
                              Q(student__lastname__icontains=query) | 
                              Q(student__program__prog_name__icontains=query) | 
                              Q(organization__name__icontains=query) | 
                              Q(organization__college__college_name__icontains=query) | 
                              Q(date_joined__icontains=query))
          return qs

class OrgMemberCreateView(CreateView):
     model = OrgMember
     form_class = OrgMemberForm
     template_name = 'orgmember_add.html'
     success_url = reverse_lazy('orgmember-list')

     def form_valid(self, form):
          org_member_firstname = form.instance.student.firstname
          org_member_lastname = form.instance.student.lastname
          org_member_org = form.instance.organization.name
          messages.success(self.request, f'{org_member_firstname} {org_member_lastname} has been successfully registered to {org_member_org}.')

          return super().form_valid(form)

class OrgMemberUpdateView(UpdateView):
     model = OrgMember
     form_class = OrgMemberForm
     template_name = 'orgmember_edit.html'
     success_url = reverse_lazy('orgmember-list')

     def form_valid(self, form):
          org_member_firstname = form.instance.student.firstname
          org_member_lastname = form.instance.student.lastname
          messages.success(self.request, f'{org_member_firstname} {org_member_lastname} has been successfully updated')

          return super().form_valid(form)

class OrgMemberDeleteView(DeleteView):
     model = OrgMember
     template_name = 'orgmember_del.html'
     success_url = reverse_lazy('orgmember-list')

#STUDENTS
class StudentList(ListView):
     model = Student
     context_object_name = 'Student'
     template_name = 'student_list.html'
     paginate_by = 5
     
     def get_queryset(self, *args, **kwargs):
        qs = super(StudentList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None: 
            query = self.request.GET.get('q') 
            qs = qs.filter(Q(student_id__icontains=query) | 
                           Q(firstname__icontains=query) |
                           Q(middlename__icontains=query) |
                           Q(lastname__icontains=query) |
                           Q(program__prog_name__icontains=query)|
                           Q(program__college__college_name__icontains=query))          
        return qs
     
class StudentCreateView(CreateView):
     model = Student
     form_class = StudentForm
     template_name = 'student_add.html'
     success_url = reverse_lazy('student-list')

     def form_valid(self, form):
          student_firstname = form.instance.firstname
          student_lastname = form.instance.lastname
          messages.success(self.request, f'{student_firstname} {student_lastname} has been successfully added.')

          return super().form_valid(form)

class StudentUpdateView(UpdateView):
     model = Student
     form_class = StudentForm
     template_name = 'student_edit.html'
     success_url = reverse_lazy('student-list')

     def form_valid(self, form):
          student_firstname = form.instance.firstname
          student_lastname = form.instance.lastname
          messages.success(self.request, f'{student_firstname} {student_lastname} has been successfully updated.')

          return super().form_valid(form)


class StudentDeleteView(DeleteView):
     model = Student
     template_name = 'student_del.html'
     success_url = reverse_lazy('student-list')

#COLLEGE
class CollegeList(ListView):
     model = College
     context_object_name = 'college'
     template_name = 'college_list.html'
     paginate_by = 5
     
     def get_queryset(self, *args, **kwargs):
        qs = super(CollegeList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None: 
            query = self.request.GET.get('q') 
            qs = qs.filter(
                Q(college_name__icontains=query))
        return qs
     
class CollegeCreateView(CreateView):
     model = College
     form_class = CollegeForm
     template_name = 'college_add.html'
     success_url = reverse_lazy('college-list')

     def form_valid(self, form):
          college_name = form.instance.college_name
          messages.success(self.request, f'{college_name} has been successfully added.')

          return super().form_valid(form)

class CollegeUpdateView(UpdateView):
     model = College
     form_class = CollegeForm
     template_name = 'college_edit.html'
     success_url = reverse_lazy('college-list')

     def form_valid(self, form):
          college_name = form.instance.college_name
          messages.success(self.request, f'{college_name} has been successfully updated.')

          return super().form_valid(form)

class CollegeDeleteView(DeleteView):
     model = College
     template_name = 'college_del.html'
     success_url = reverse_lazy('college-list')

#PROGRAM
class ProgramList(ListView):
     model = Program
     context_object_name = 'program'
     template_name = 'program_list.html'
     paginate_by = 5
     
     def get_queryset(self, *args, **kwargs):
        qs = super(ProgramList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None: 
            query = self.request.GET.get('q') 
            qs = qs.filter(Q(prog_name__icontains=query) |
                           Q(college__college_name__icontains=query))
        return qs
     
class ProgramCreateView(CreateView):
     model = Program
     form_class = ProgramForm
     template_name = 'program_add.html'
     success_url = reverse_lazy('program-list')

     def form_valid(self, form):
          prog_name = form.instance.prog_name
          messages.success(self.request, f'{prog_name} has been successfully added.')

          return super().form_valid(form)
     
class ProgramUpdateView(UpdateView):
     model = Program
     form_class = ProgramForm
     template_name = 'program_edit.html'
     success_url = reverse_lazy('program-list')

     def form_valid(self, form):
          prog_name = form.instance.prog_name
          messages.success(self.request, f'{prog_name} has been successfully updated.')

          return super().form_valid(form)
     
class ProgramDeleteView(DeleteView):
     model = Program
     template_name = 'program_del.html'
     success_url = reverse_lazy('program-list')

def multipleBarbyCollege(request): #counts organization per college
    query = ''' 
    SELECT  
        c.college_name, 
        COUNT(o.id) AS org_count 
    FROM  
        app_organization o 
    INNER JOIN app_college c ON o.college_id = c.id 
    GROUP BY c.college_name 
    ORDER BY c.college_name 
    ''' 
    with connection.cursor() as cursor: 
        cursor.execute(query) 
        rows = cursor.fetchall() 
 
    result = {} 

    # Process the rows into a dictionary
    for row in rows: 
        college_name = row[0] 
        org_count = row[1] 
 
        # Populate the result with the college name and organization count
        result[college_name] = org_count 
 
    return JsonResponse(result)



