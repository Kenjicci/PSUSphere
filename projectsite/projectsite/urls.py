from django.contrib import admin
from django.urls import path, re_path
from studentorg.views import (
HomePageView, OrganizationList, OrganizationCreateView, OrganizationUpdateView, OrganizationDeleteView,
OrgMemberList, OrgMemberCreateView, OrgMemberUpdateView, OrgMemberDeleteView,
StudentList, StudentCreateView, StudentUpdateView, StudentDeleteView,
CollegeList, CollegeCreateView, CollegeUpdateView, CollegeDeleteView,
ProgramList, ProgramCreateView, ProgramUpdateView, ProgramDeleteView,
ChartView, BarCountStudentperCollege, PieOrgperCollege, LineActivities,
ScatterTopOrganizations
)
from studentorg import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path("admin/", admin.site.urls),
    path('', HomePageView.as_view(), name='home'), 
    path('dashboard_chart', ChartView.as_view(), name="dashboard-chart"),
    path('bar-count-student-per-college/', BarCountStudentperCollege, name='chart'),
    path('pie-org-per-college/', PieOrgperCollege, name='chart'),
    path('line-activities-by-month/', LineActivities, name='chart'),
    path('scatter-top-organizations/', ScatterTopOrganizations, name='chart'),
    path('student-enrollment-by-year/', views.student_enrollment_by_year, name='student_enrollment_by_year'),
    
    
    
    
    path('organization_list/', OrganizationList.as_view(), name='organization-list'),
    path('organization_list/add/', OrganizationCreateView.as_view(), name='organization-add'),
    path('organization_list/organization_list/<pk>/', OrganizationUpdateView.as_view(), name='organization-update'),
    path('organization_list/organization_list/<pk>/delete/', OrganizationDeleteView.as_view(), name='organization-delete'),
    path('orgmember_list/', OrgMemberList.as_view(), name='orgmember-list'),
    path('orgmember_list/add/', OrgMemberCreateView.as_view(), name='orgmember-add'),
    path('orgmember_list/orgmember_list/<pk>/', OrgMemberUpdateView.as_view(), name='orgmember-update'),
    path('orgmember_list/orgmember_list/<pk>/delete/', OrgMemberDeleteView.as_view(), name='orgmember-delete'),
    path('student_list/', StudentList.as_view(), name='student-list'),
    path('student_list/add/', StudentCreateView.as_view(), name='student-add'),
    path('student_list/student_list/<pk>/', StudentUpdateView.as_view(), name='student-update'),
    path('student_list/student_list/<pk>/delete/', StudentDeleteView.as_view(), name='student-delete'),
    path('college_list/', CollegeList.as_view(), name='college-list'),
    path('college_list/add/', CollegeCreateView.as_view(), name='college-add'),
    path('college_list/college_list/<pk>/', CollegeUpdateView.as_view(), name='college-update'),
    path('college_list/college_list/<pk>/delete/', CollegeDeleteView.as_view(), name='college-delete'),
    path('program_list/', ProgramList.as_view(), name='program-list'),
    path('program_list/add/', ProgramCreateView.as_view(), name='program-add'),
    path('program_list/program_list/<pk>/', ProgramUpdateView.as_view(), name='program-update'),
    path('program_list/program_list/<pk>/delete/', ProgramDeleteView.as_view(), name='program-delete'),
    re_path(r'^login/$', auth_views.LoginView.as_view(
        template_name='login.html'), name='login'), 
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'), 
]
