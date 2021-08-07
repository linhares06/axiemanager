#from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import (DeleteView, ListView, DetailView, CreateView)
from django.views.generic.edit import DeleteView, UpdateView

from manager.forms import AxieForm, StudentForm
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

    axie_form = AxieForm()

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AxieCreateView, self).get_form_kwargs()
        kwargs["user_id"] = self.request.user.pk
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AxieCreateView, self).get_context_data(**kwargs)
        context["axie_form"] = self.axie_form
        context["axie_form"].fields["user"].initial = self.request.user.pk
        return context

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
    form_class = AxieForm
    model = Student

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/"
    form_class = StudentForm
    model = Student

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "/"
    model = Student
    success_url = reverse_lazy("student_list")

## Classes related to Payment
class PaymentListView(LoginRequiredMixin, ListView):
    login_url = "/"
    model = Payment

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

#def get_json_from_ronin_id(request):
#
#    r = requests.get(url='https://api.lunaciarover.com/stats/0x36ec27579284e7fd3b6bf43a937bcc23aaaef1a4')
#    return HttpResponse((r.json()))