from django import forms
from django.db.models import fields
from django.forms import widgets
from django.contrib.auth.models import User
from manager.models import Payment, ScholarshipOwner, Student, Axie

class StudentForm(forms.ModelForm):

    class Meta():
        model = Student
        fields = ("name", "email", "current_slp", "active", "observarion")

class AxieForm(forms.ModelForm):

    class Meta():
        model = Axie
        fields = ("axie_id", "student", "buy_date", "description", "eth_cost", "sold", "user")

    def __init__(self, *args, user_id=None, **kwargs):
        super(AxieForm, self).__init__(*args, **kwargs)
        self.fields["student"].queryset = Student.objects.filter(user_id=user_id)
        self.fields["user"].queryset = User.objects.filter(id=user_id)
        self.fields['user'].empty_label = None

class PaymentForm(forms.ModelForm):

    class Meta():
        model = Payment
        fields = ("student", "value")