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

    # Testing how to limit access to objects from diferent users, this may be a solution
    #def get_object(self, queryset=None):
     #   return self.model.objects.get(pk=self.request.user.pk)
      #  if queryset is None:
       #     queryset = self.get_queryset()   

        #queryset = queryset.filter(user_id=self.request.user.pk)

        #try:
         #   obj = queryset.get()
        #except queryset.model.DoesNotExist:
        #    return HttpResponse("No user matching this query")
        #return obj

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
    # For some reason, you need to explicitly tell django the 'template_name' when working with multiple ListViews with the same model
    template_name = "manager/buyandsell_list.html"
    login_url = "/"
    model = Axie

    def get_queryset(self):
        return Axie.objects.filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ## !!! calculating sum is returning a float value, and result is wrong, need to understand it better
        total_eth = Axie.objects.filter(Q(user_id=self.request.user.id) | Q(sold=0)).aggregate(Sum("eth_cost"))
        # better understand the format function to format the value with the right amount of numbers after the coma
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
            #TODO: bad response, figure sothing else to return to client
            return HttpResponse("Invalid Login")
    else:
        return render(request, "manager/login.html", {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("user_login"))

def get_json_from_ronin_id(request, pk):

#    r = requests.get(url='https://api.lunaciarover.com/stats/0x36ec27579284e7fd3b6bf43a937bcc23aaaef1a4')
#   json return for test
    r = '{"ronin_address": "0x36ec27579284e7fd3b6bf43a937bcc23aaaef1a4", "updated_on": 1630014640, "last_claim_amount": 4305, "last_claim_timestamp": 1629344555, "ronin_slp": 0, "total_slp": 1026, "in_game_slp": 1026, "slp_success": true, "rank": 22324, "mmr": 1882, "total_matches": 0, "win_rate": 0, "ign": "Paulo Gomes", "game_stats_success": true}'
    json_value = json.loads(r)
    
    student = Student.objects.get(id=pk)
    student.total_slp = json_value["total_slp"]
    student.save()

    #TODO: figure how to send update message
    #messages.success(request, 'Form submission successful')
          
    return HttpResponseRedirect(reverse("student_list"))