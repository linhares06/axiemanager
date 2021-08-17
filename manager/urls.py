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
    path('student/new/', views.StudentCreateView.as_view(), name="student_form"),
    path('student/update/<int:pk>/', views.StudentUpdateView.as_view(), name="student_update"),
    path('student/delete/<int:pk>/', views.StudentDeleteView.as_view(), name="student_delete"),
    ## paths to payments
    path('payment/', views.PaymentListView.as_view(), name="payment_list"),
    path('payment/<int:pk>/', views.PaymentDetailView.as_view(), name="payment_detail"),
    path('payment/new/', views.PaymentCreateView.as_view(), name="payment_form"),
    path('payment/update/<int:pk>/', views.PaymentUpdateView.as_view(), name="payment_update"),
    path('payment/delete/<int:pk>/', views.PaymentDeleteView.as_view(), name="payment_delete"),
    ## paths to Buy and Sell
    path('buyandsell/', views.BuyAndSellListView.as_view(), name="buyandsell_list"),
]