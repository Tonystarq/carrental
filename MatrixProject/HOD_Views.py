import dis
import json
from multiprocessing import context

from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from matrixapp.models import *
from django.contrib import messages
import csv
import datetime


import MySQLdb




     
 


@login_required(login_url='/')
def HOME(request):
    
    return render(request, 'HOD/home.html')

def  cancelledplote(request):
    return render(request, 'HOD/cancelledplote.html')

def  bookingdetails(request):
    return render(request, 'HOD/bookingdetail.html')




def  addcar(request):
    if request.method == "POST":
        VehicleModel = request.POST.get("VehicleModel")
        VehicleNumber = request.POST.get("VehicleNumber")
        SeatingCapacity = request.POST.get("SeatingCapacity")
        RentPerDay = request.POST.get("RentPerDay")
       
        
        add_car= AddCar(VehicleModel= VehicleModel,VehicleNumber = VehicleNumber, SeatingCapacity = SeatingCapacity,RentPerDay=RentPerDay)
       
       
        
        if AddCar.objects.filter(VehicleNumber = VehicleNumber).exists():
            messages.warning(request, "Car No. is already Taken")
            return redirect('addcar')
        
        add_car.save()

        
    return render(request, 'HOD/addcar.html')

def view_Car(request):
    VehicleNumber = AddCar.objects.all()
    return render(request,'HOD/view_Car.html',{'VehicleNumber':VehicleNumber})    


def availablecar(request):
    VehicleNumber = AddCar.objects.all()
    return render(request,'HOD/availablecars.html',{'VehicleNumber':VehicleNumber})  



def EDIT_Car(request,id): 
    VehicleNumber = AddCar.objects.filter(id=id)
    context = {
        'VehicleNumber':VehicleNumber

        
    }
    return render(request, 'HOD/editcar.html', context)    
   





def UpdateCar(request):
    if request.method == "POST":
        VehicleModel = request.POST.get("VehicleModel")
        vehicleid=request.POST.get("vehicleid")
        VehicleNumber = request.POST.get("VehicleNumber")
        SeatingCapacity = request.POST.get("SeatingCapacity")
        RentPerDay = request.POST.get("RentPerDay")
        
       
       
        Vehicle = AddCar.objects.get(id=vehicleid)
        Vehicle.VehicleNumber = VehicleNumber
        Vehicle.VehicleModel = VehicleModel
        Vehicle.SeatingCapacity = SeatingCapacity
        Vehicle.RentPerDay = RentPerDay
       
        
       
        Vehicle.save()
        messages.success(request, "Record Updated Add Successfully")
        return redirect('view_Car')
    return render(request,"HOD/editcar.html")


def deletecar(request,id):

    VehicleNumber = AddCar.objects.get(id=id)
    
    VehicleNumber.delete()
    messages.success(request,"Record are Successfully Deleted")
    return redirect('view_Car')
         

@login_required(login_url='/')
def  BookCar(request):
   
    selected_customer_id = None
    selected_plot_no = None
    customer_Id = Customer.objects.all()
    plot_no = AddCar.objects.all()
    current_user = request.user
    code = current_user.user_id
    
    rank = current_user.rank
    plot_number = AddCar.objects.all()

  
  
    

    if request.method =="POST":
        if 'newsletter_sub' in request.POST:
        
            selected_customer_id = request.POST.get("user_id")
            customer_Id = customer_Id.filter(customer_id=selected_customer_id)

            selected_plot_no = request.POST.get("plot_no")
            plot_no = plot_no.filter(plot_no=selected_plot_no)
        if 'demo' in request.POST:

        
            ref_id = request.POST.get('ref_id')
        
            user_id = request.POST.get('user_id')
        
            plot_number = request.POST.get('plot_number')
            amount = int(request.POST.get('amount'))
            booking_amount = int(request.POST.get('booking_amount'))
            remaining_amount = amount-booking_amount
            name = request.POST.get('name')
            father_name = request.POST.get('father_name')
            mobile_number = request.POST.get('mobile_number')
            payment_mode = request.POST.get('payment_mode')
            remarks = request.POST.get('remarks')
            receipt = request.FILES.get('receipt')
            plot_size = request.POST.get('plot_size')
            mail = request.POST.get('mail')
            addresss = request.POST.get('addresss')
            print(ref_id)

            book_plot = BookCar(ref_id= ref_id,user_id=user_id,plot_number = plot_number, Payable_amout = amount,payment_amount=booking_amount,remaining_amount=remaining_amount, name = name,father_name = father_name , mobile_no = mobile_number, payment_mode = payment_mode ,remarks=remarks,receipt=receipt ,plot_size=plot_size,addresss=addresss,mail=mail)
            owner=book_plot.owner=request.user
            book_plot.owner = owner


            isntallment = BookCar(ref_id= ref_id,user_id=user_id,plot_number = plot_number, Payable_amout = amount,payment_amount = booking_amount,remaining_amount=remaining_amount,name = name, mobile_no = mobile_number, payment_mode = payment_mode ,remarks=remarks,receipt=receipt,plot_size=plot_size ,addresss=addresss,mail=mail)
            owner=isntallment.owner=request.user
            isntallment.owner = owner
            if BookCar.objects.filter(plot_number = plot_number).exists():
                messages.warning(request, "Plot Number is already Taken")
                return redirect('BookCar')
            
            
            book_plot.save()
            isntallment.save()
            messages.success(request,"Booking Plot Successfully")
            return redirect('BookCar')
    cus_id = Customer.objects.order_by('customer_id').values_list('customer_id', flat=True)
    plot_num = AddCar.objects.order_by('plot_no').values_list('plot_no', flat=True)
        

    context = {
    'code':code,
    'rank':rank,
    'plot_number':plot_number,
    'cus_id':cus_id,
    'customer_Id':customer_Id,
    'selected_customer_id':selected_customer_id,
    'plot_num':plot_num,
    'plot_no':plot_no,
    'selected_plot_no':selected_plot_no,
    
   

    }
    return render(request, 'HOD/BookCar.html', context)


def  approvedplote(request):
    
    booking_data = BookCar.objects.all()
   

    context = {
        'booking_data': booking_data,
        
        
      

    }
    

    return render(request, 'HOD/approvedplote.html', context)


def EDIT_BookCar(request,id):
    BookCar = BookCar.objects.filter(id=id)
    cust_id = Customer.objects.all()   
    plot_no = AddCar.objects.all()  
    context = {
        'BookCar': BookCar,
        'plot_no':plot_no,
        'cust_id':cust_id
        
    }
    return render(request, 'HOD/editBookCar.html', context)


def DELETE_PLOT(request,id):

    plot = BookCar.objects.get(id=id)
    
    plot.delete()
    messages.success(request,"Record are Successfully Deleted")
    return redirect('approvedplote')


def SEARCH_BAR(request):
    if request.method == "POST":
        searched = request.POST['searched']
        venues = Customer.objects.filter(customer_id__contains=searched)

        return render(request, 'search.html',{'searched':searched,'venues':venues})
    else:
        return render(request, 'search.html',{})




def UPDATE_BookCar(request):
    if request.method == "POST":
        BookCar_id = request.POST.get('BookCar_id')
        print(BookCar_id)
        ref_id = request.POST.get('ref_id')
        user_id = request.POST.get('user_id')
       
        plot_number = request.POST.get('plot_number')
        amount = request.POST.get('amount')
        Mnthly_BookCar = request.POST.get('Mnthly_BookCar')
        no_BookCar = request.POST.get('no_BookCar')
        name = request.POST.get('name')
        father_name = request.POST.get('father_name')
        mobile_number = request.POST.get('mobile_number')
        payment_mode = request.POST.get('payment_mode')
        remarks = request.POST.get('remarks')
        receipt = request.FILES.get('receipt')
        print(ref_id)
        BookCar = BookCar.objects.get(id=BookCar_id)

        BookCar.plot_number = plot_number
        BookCar.Payable_amout = amount
        BookCar.Mnthly_BookCar = Mnthly_BookCar
        BookCar.number_of_BookCar = no_BookCar
        BookCar.name = name
        BookCar.father_name = father_name
        BookCar.mobile_no = mobile_number
        BookCar.payment_mode = payment_mode
        BookCar.remarks = remarks
        BookCar.receipt = receipt
        BookCar.save()
        messages.success(request, "Record Are Successfully Updated")
        return redirect('approvedplote')

        
    return render(request, 'HOD/edit_student.html')    



    

