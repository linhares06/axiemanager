#from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.http.response import Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import (DeleteView, ListView, DetailView, CreateView)
from django.views.generic.edit import DeleteView, UpdateView
from django.db.models import Sum, Q
from django.contrib import messages

import json

from manager.forms import AxieForm, PaymentForm, StudentForm
from manager.models import Axie, Payment, ScholarshipOwner, Student

## Classes related to Axie
class AxieListView(LoginRequiredMixin, ListView):
    login_url = "/"
    model = Axie

    def get_queryset(self):
        return Axie.objects.filter(user_id=self.request.user.id)

class AxieDetailView(LoginRequiredMixin, DetailView):
    login_url = "/"
    model = Axie

class AxieCreateView(LoginRequiredMixin, CreateView):
    login_url = "/"
    form_class = AxieForm
    model = Axie

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AxieCreateView, self).get_form_kwargs()
        kwargs["user_id"] = self.request.user.pk
        return kwargs

class AxieUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/"
    form_class = AxieForm
    model = Axie

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AxieUpdateView, self).get_form_kwargs()
        kwargs["user_id"] = self.request.user.pk
        return kwargs

class AxieDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "/"
    model = Axie
    success_url = reverse_lazy("axie_list")

## Classes related to Student
class StudentListView(LoginRequiredMixin, ListView):
    login_url = "/"
    model = Student

    def get_queryset(self):
        return Student.objects.filter(user_id=self.request.user.id)

class StudentDetailView(LoginRequiredMixin, DetailView):
    login_url = "/"
    model = Student

class StudentCreateView(LoginRequiredMixin, CreateView):
    login_url = "/"
    form_class = StudentForm
    model = Student

    def get_form_kwargs(self, **kwargs):
        kwargs = super(StudentCreateView, self).get_form_kwargs()
        kwargs["user_id"] = self.request.user.pk
        return kwargs

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/"
    form_class = StudentForm
    model = Student

    def get_form_kwargs(self, **kwargs):
        kwargs = super(StudentUpdateView, self).get_form_kwargs()
        kwargs["user_id"] = self.request.user.pk
        return kwargs

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "/"
    model = Student
    success_url = reverse_lazy("student_list")

## Classes related to Payment
class PaymentListView(LoginRequiredMixin, ListView):
    login_url = "/"
    model = Payment

    def get_queryset(self):
        return Payment.objects.filter(user_id=self.request.user.id)

class PaymentDetailView(LoginRequiredMixin, DetailView):
    login_url = "/"
    model = Payment

class PaymentCreateView(LoginRequiredMixin, CreateView):
    login_url = "/"
    form_class = PaymentForm
    model = Payment

    def get_form_kwargs(self, **kwargs):
        kwargs = super(PaymentCreateView, self).get_form_kwargs()
        kwargs["user_id"] = self.request.user.pk
        return kwargs

class PaymentUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/"
    form_class = PaymentForm
    model = Payment

    def get_form_kwargs(self, **kwargs):
        kwargs = super(PaymentUpdateView, self).get_form_kwargs()
        kwargs["user_id"] = self.request.user.pk
        return kwargs

class PaymentDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "/"
    model = Payment
    success_url = reverse_lazy("payment_list")

## Classes related Buy and Sell
class BuyAndSellListView(LoginRequiredMixin, ListView):
    
    template_name = "manager/buyandsell_list.html"
    login_url = "/"
    model = Axie

    def get_queryset(self):
        return Axie.objects.filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        total_eth = Axie.objects.filter(Q(user_id=self.request.user.id) | Q(sold=0)).aggregate(Sum("eth_cost"))
        
        context["total_eth"] = "{0:.10g}".format(total_eth["eth_cost__sum"])

        sold_total_eth = Axie.objects.filter(Q(user_id=self.request.user.id) | Q(sold=1)).aggregate(Sum("eth_cost"))
        context["sold_total_eth"] = "{0:.10g}".format(sold_total_eth["eth_cost__sum"])

        return context

## Methods related to login and logout
def user_login(request):

    if request.method == "POST":
        
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("axie_list"))
                #TODO: change to:
                #return HttpResponseRedirect(reverse("home"))
            else:
                #TODO: Maybe massage about paying for access and letting download csv
                return HttpResponse("ACC NOT ACTIVE")
        else:
            
            return HttpResponse("Invalid Login")
    else:
        return render(request, "manager/login.html", {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("user_login"))

def get_json_from_ronin_id(request, pk):

    r = requests.get(url='https://api.lunaciarover.com/stats/0x36ec27579284e7fd3b6bf43a937bcc23aaaef1a4')

   json_value = json.loads(r)
    
    student = Student.objects.get(id=pk)
    student.total_slp = json_value["total_slp"]
    student.save()

    #TODO: figure how to send update message
    #messages.success(request, 'Form submission successful')
          
    return HttpResponseRedirect(reverse("student_list"))
