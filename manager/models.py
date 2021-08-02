from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

# Function to validate max axie per studant
def validate_axie_limit(value):
    i = 0
    for p in Axie.objects.raw('SELECT * FROM manager_axie WHERE student_id = '+str(value)):
        i += 1
    if i >= 3:
        raise ValidationError("max axie per sutdent 3")

class Student(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    start_date = models.DateField(blank=True, null=True)
    current_slp = models.PositiveIntegerField(default=0)
    total_slp = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=False)
    observarion = models.TextField(blank=True, null=True)
    ronin_id = models.CharField(max_length=42, null=True, blank=True)
    #Obs. maybe it's good to store data values for some calculations: on_delete
    owner = models.ForeignKey("manager.ScholarshipOwner", related_name="students", on_delete=models.DO_NOTHING)

    def start_scholarship(self):
        self.start_date = timezone.now()
        self.active = True
        self.save()

    def deactivate_scholarship(self):
        #TODO: remove axies from student
        self.active = False
        self.save()

    def sum_total_slp(self):
        self.total_slp += self.current_slp
        self.save()

    def add_current_slp(self):
        pass

    def subtract_current_slp(self):
        pass

    def show_axies(self):
        pass

    def update_studant_progress(self):
        #TODO: ??
        pass

    def get_absolute_url(self):
        return reverse("student_detail", kwargs={"pk":self.pk})

    def __str__(self):
        return self.name

class Axie(models.Model):
    student = models.ForeignKey("manager.Student", related_name="axies", on_delete=models.SET_NULL, blank=True, null=True, validators=[validate_axie_limit])
    axie_id = models.CharField(max_length=50)
    buy_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    eth_cost = models.DecimalField(max_digits=18, decimal_places=9, validators=[MinValueValidator(0)])
    sold = models.BooleanField(default=False)

    def sell(self):
        #TODO: verify if any Student using this axie to mark as sold
        pass

    def get_absolute_url(self):
        return reverse("axie_detail", kwargs={"pk":self.pk})

    def __str__(self):
        return self.axie_id

class Payment(models.Model):
    #Obs. maybe it's good to store values of payment and not delete cascade
    student = models.ForeignKey("manager.Student", related_name="payments", on_delete=models.DO_NOTHING)
    date = models.DateField(default=timezone.now())
    tax = models.DecimalField(max_digits=12, decimal_places=6, validators=[MinValueValidator(0)])
    value = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    total_value = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0, validators=[MinValueValidator(0)])
    slp = models.PositiveIntegerField(null=False)

    def __str__(self):
        return str(self.date) + " " + str(self.student)

class ScholarshipOwner(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #username = models.CharField(max_length=50)
    #password = models.CharField(max_length=32)
    #name = models.CharField(max_length=200)
    #email = models.EmailField(max_length=100)
    #join_date = models.DateField(blank=True, null=True, default=timezone.now())
    last_payment_date = models.DateField(blank=True, null=True)
    ronin_id = models.CharField(max_length=42, null=True, blank=True)

    def __str__(self):
        return self.user.username