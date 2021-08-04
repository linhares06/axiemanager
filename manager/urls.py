from django.urls import path
from manager import views

urlpatterns = [
    ## paths to axies
    path('axie/', views.AxieListView.as_view(), name="axie_list"),
    path('axie/<int:pk>/', views.AxieDetailView.as_view(), name="axie_detail"),
    path('axie/new/', views.AxieCreateView.as_view(), name="axie_form"),
    path('axie/update/<int:pk>/', views.AxieUpdateView.as_view(), name="axie_update"),
    path('axie/delete/<int:pk>/', views.AxieDeleteView.as_view(), name="axie_delete"),
    ## paths to students
    path('student/', views.StudentListView.as_view(), name="student_list"),
    path('student/<int:pk>/', views.StudentDetailView.as_view(), name="student_detail"),
    ## paths to payments
    path('payment/', views.PaymentListView.as_view(), name="payment_list"),
]