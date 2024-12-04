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

from django.db.models.functions import TruncMonth
from django.http import JsonResponse

from django.contrib import messages
from datetime import datetime
from django.db.models import Count, Avg
from django.db.models.functions import ExtractMonth


@method_decorator(login_required, name="dispatch")
class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"

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
          messages.success(self.request, f'{org_name} has been added.')

          return super().form_valid(form)


class OrganizationUpdateView(UpdateView):
     model = Organization
     form_class = OrganizationForm
     template_name = 'org_edit.html'
     success_url = reverse_lazy('organization-list')

     def form_valid(self, form):
          org_name = form.instance.name
          messages.success(self.request, f'{org_name} has been updated.')

          return super().form_valid(form)
     
class OrganizationDeleteView(DeleteView):
     model = Organization
     # form_class = OrganizationForm
     template_name = 'org_del.html'
     success_url = reverse_lazy('organization-list')

     def form_valid(self, form):
          messages.success(self.request, 'Deleted successfully.')
          return super().form_valid(form)

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
          messages.success(self.request, f'{org_member_firstname} {org_member_lastname} has registered to {org_member_org}.')

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

     def form_valid(self, form):
          messages.success(self.request, 'Deleted successfully')
          return super().form_valid(form)

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

     def form_valid(self, form):
          messages.success(self.request, 'Deleted successfully')
          return super().form_valid(form)

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

     def form_valid(self, form):
          messages.success(self.request, 'Deleted successfully')
          return super().form_valid(form)

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

     def form_valid(self, form):
          messages.success(self.request, 'Deleted successfully')
          return super().form_valid(form)

class ChartView(ListView):
    template_name = 'chart.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        pass

def BarCountStudentperCollege(request):
    data = (
        Student.objects.values('program__college__college_name')
        .annotate(count=Count('id'))
        .order_by('program__college__college_name')
    )

    if not data:
        return JsonResponse({
            'labels': [],
            'series': []
        })

    chart_data = {
        'labels': [item['program__college__college_name'] for item in data],
        'series': [item['count'] for item in data]
    }

    return JsonResponse(chart_data)

def PieOrgperCollege(request):
     data = (
          Organization.objects.values('college__college_name')
          .annotate(count=Count('id'))
          .order_by('-count')
     )

     chart_data = {
        'labels': [item['college__college_name'] for item in data],
        'series': [item['count'] for item in data],
    }
     
     return JsonResponse(chart_data)
 
 
def LineActivities(request):
    data = (
        OrgMember.objects.filter(date_joined__year=2024)
        .annotate(month=ExtractMonth('date_joined'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    # Prepare data for all months
    activity_data = {item['month']: item['count'] for item in data}
    all_months = range(1, 13)  # Ensure data for all 12 months
    complete_data = {month: activity_data.get(month, 0) for month in all_months}

    chart_data = {
        'labels': [datetime(2024, month, 1).strftime('%b') for month in complete_data.keys()],
        'series': [[count for count in complete_data.values()]],  # Wrap count in a list
    }

    return JsonResponse(chart_data)

def ScatterTopOrganizations(request):
    data = (
        Organization.objects
        .annotate(member_count=Count('orgmember'))  #
        .order_by('-member_count')
        .values('name', 'member_count')[:6]  # Get the top 6 organizations by member count
    )
    
    # Prepare data for the scatter chart
    labels = [entry['name'] for entry in data]  
    member_counts = [entry['member_count'] for entry in data] 
    

    return JsonResponse({'labels': labels, 'member_counts': member_counts})