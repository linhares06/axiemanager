#from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import (DeleteView, ListView, DetailView, CreateView)
from django.views.generic.edit import DeleteView, UpdateView

#import requests

from manager.forms import AxieForm, StudentForm
from manager.models import Axie, Student

# TODO: learn
def create_and_update_axie(model):
    login_url = "/login/"
    redirect_field_name = "manager/home.html"
    form_class = AxieForm
    model = Axie

## Classes related to Axie
class AxieListView(LoginRequiredMixin, ListView):
    login_url = "/"
    model = Axie

class AxieDetailView(LoginRequiredMixin, DetailView):
    login_url = "/"
    model = Axie

class AxieCreateView(LoginRequiredMixin, CreateView):
    login_url = "/"
    form_class = AxieForm
    model = Axie

class AxieUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/"
    form_class = AxieForm
    model = Axie

class AxieDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "/"
    model = Axie
    success_url = reverse_lazy("axie_list")

## Classes related to Student
class StudentListView(LoginRequiredMixin, ListView):
    login_url = "/"
    model = Student

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