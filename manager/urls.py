from django.urls import path
from manager import views

urlpatterns = [
    ## paths to axies
    path('axie/', views.AxieListView.as_view(), name="axie_list"),
    path('axie/<int:pk>/', views.AxieDetailView.as_view(), name="axie_detail"),
    path('axie/new/', views.AxieCreateView.as_view(), name="axie_new"),
    path('axie/<int:pk>/edit/', views.AxieUpdateView.as_view(), name="axie_edit"),
    path('axie/<int:pk>/remove/', views.AxieDeleteView.as_view(), name="axie_remove"),
    ## paths to students
    path('student/', views.StudentListView.as_view(), name="student_list"),
    path('student/<int:pk>/', views.StudentDetailView.as_view(), name="student_detail"),
]