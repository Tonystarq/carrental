import email
from django.shortcuts import render,redirect,HttpResponse
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from matrixapp import views
from MatrixProject import settings

from .import *
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from matrixapp.models import *
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
import csv
import datetime


@login_required(login_url='/')
def Home(request):
    

    return render(request, 'AGENT/home.html')
def view_Car1(request):
    VehicleNumber = AddCar.objects.all()
    return render(request,'AGENT/view_Car1.html',{'VehicleNumber':VehicleNumber})
    
@login_required(login_url='/')
def  bookcar(request, id):

    VehicleNumber = AddCar.objects.filter(id=id)
    current_user = request.user
    code = current_user.user_id
    context = {
        'code':code,
        'VehicleNumber':VehicleNumber

        
    }
        

    return render(request, 'AGENT/bookcar.html', context)

def  bookcar1(request):
    if request.method == "POST":
        VehicleModel = request.POST.get('VehicleModel')
        
       
        
        VehicleNumber = request.POST.get('VehicleNumber')
        SeatingCapacity =request.POST.get('SeatingCapacity')
        RentPerDay = request.POST.get('RentPerDay')
        ref_id = request.POST.get('ref_id')
        date1 = request.POST.get('date1')
        date2 = request.POST.get('date2')
           
        bookcar = BookCar(VehicleModel= VehicleModel,VehicleNumber = VehicleNumber, SeatingCapacity = SeatingCapacity,RentPerDay=RentPerDay,ref_id=ref_id,date1=date1,date2=date2)
       
       
        
           


        
            
        bookcar.save()
            
        messages.success(request,"Booking Car Successfully")
        return redirect('view_Car1')
        
    return render(request, 'AGENT/view_Car1.html')

def bookedcars(request):
    VehicleNumber = BookCar.objects.all()
    
    current_user = request.user

    Agent_code = current_user
    code = Agent_code.user_id
    context = {
        'customer' : VehicleNumber,
        'code' : code
    }

   
    return render(request,'AGENT/bookedcars.html',context)