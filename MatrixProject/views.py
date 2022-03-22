from asyncore import write
from multiprocessing import context
from operator import imod
from urllib import response
from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from MatrixProject.SuperAgent_Views import Home
from matrixapp.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
from matrixapp.models import *
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import csv
import datetime


def export_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    
    response['Content-Disposition'] = 'attachment; filename= Booking Details'+ str(datetime.datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Father Name', 'Plot No', 'Amount', 'Payment Mode', 'Mobile No', 'Ref Id', 'Date', 'Remarks'])
    approve_plot = BookCar.objects.all()
    for approve in approve_plot:
        print(approve)
    
        writer.writerow(
                    [approve.name, 
				approve.father_name, 
				approve.plot_number, 
				approve.Payable_amout, 
				approve.payment_mode, 
				approve.mobile_no, 
				approve.ref_id, 
				approve.joinig_date, 
				approve.remarks])
           

    return response


def BASE(request):
    return render(request, 'base.html')



def BASE1(request):
    return render(request, 'base1.html')




def pagelogin(request):
    return render(request, 'page-login.html')

def pagelogin1(request):
    return render(request, 'page-login1.html')
def prelogin(request):
    return render(request, 'prelogin.html')

def frontend(request):
    return render(request, 'default/in.html')


def signup_admin(request):
    return render(request,"HOD/signup_admin_page.html")



def do_admin_signup(request):
    username=request.POST.get("username")
    fname=request.POST.get("fname")
    lname=request.POST.get("lname")
    email=request.POST.get("email")
    password=request.POST.get("password")
    rpt_password=request.POST.get("rpt_password")
    

    if password != rpt_password:
        messages.error(request,"Password does not match")
        return redirect('signup_admin')

   
    user=CustomUser.objects.create_user(username=username,email=email,password=password,user_type=1)
    user.first_name = fname
    user.last_name = lname
    

      


    user.save()
    hod = HOD(
                admin = user,  
                # rank = rank                      
            )
    hod.save()
    
    
    messages.success(request,"Successfully Created Admin")
    return HttpResponseRedirect(reverse("login"))
    

@login_required
def dosuperAgent(request):
    current_user = request.user
    code = current_user.user_id
    rank = current_user.rank
  
  
    if request.method == "POST":
        username=request.POST.get("username")
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        email=request.POST.get("email")
        password1=request.POST.get("password1")        
        password2=request.POST.get("password2")
        Refrence_ID=request.POST.get("Refrence_ID")
        percentage=request.POST.get("percentage")
 
     
        # print(profile_pic,first_name,last_name,email,username,password,address,gender,course_id,session_year_id)

        if CustomUser.objects.filter(email = email).exists():
            messages.warning(request, "Email is already Taken")
            return redirect('registeruser')

        if CustomUser.objects.filter(username = username).exists():
            messages.warning(request, "Username is already Taken")
            return redirect('Agent_Home')
        
        else:
            user = CustomUser(
                first_name = fname,
                last_name = lname,
                username = username,
                email = email,               
                user_type = 2,
                rank = percentage,
                
                
            )
            if password1!=password2:

                messages.warning(request, "Password Does not match")
                return redirect('registeruser')
            
            user.set_password(password1)
            user.save()

            
            agent = SuperAgent(
                admin = user,
                # rank = rank,
                reference_id = Refrence_ID              
 
            )
            agent.save()
            messages.success(request, user.first_name + "  "+ user.last_name + ' Are Successfully Added !!' )
            return redirect('admin_home')
    context = {
        'code':code,
        'rank':rank
    }

    return render(request, 'register-user.html',context)


def doAgent(request):

    if request.method == "POST":
        username=request.POST.get("username")
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        email=request.POST.get("email")
        password1=request.POST.get("password1")        
        password2=request.POST.get("password2")
       
      
 
     
        

        if CustomUser.objects.filter(email = email).exists():
            messages.warning(request, "Email is already Taken")
            return redirect('registeruserr')

        if CustomUser.objects.filter(username = username).exists():
            messages.warning(request, "Username is already Taken")
            return redirect('registeruserr')
        
        else:
            user = CustomUser(
                first_name = fname,
                last_name = lname,
                username = username,
                email = email,               
                user_type = 2,
               
                
                
            )
            if password1!=password2:

                messages.warning(request, "Password Does not match")
                return redirect('registeruserr')
            
            user.set_password(password1)
            user.save()

            
            agent = SuperAgent(
                admin = user,
                
                
            )
            agent.save()
            messages.success(request, user.first_name + "  "+ user.last_name + ' Are Successfully Added !!' )
            return redirect('Agent_Home')
    

    return render(request, 'register-userr.html')
      



def doLogin(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password = request.POST.get('password'))
        if user!=None:
            login(request,user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('admin_home')
             
                
            
            else:
                
                
                messages.error(request,"This is not correct Login Or Password as Admin")
        else:
            messages.error(request,"Invalid Login Or Password!!")
            
            
            return redirect('login')
        
    return render(request, 'page-login.html')

def doLogin1(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password = request.POST.get('password'))
        if user!=None:
            login(request,user)
            user_type = user.user_type
            
                
            if user_type == '2':
                
                return redirect('Agent_Home')
        
            
            else:
                
                messages.error(request,"This is not correct Login Or Password as Agent")
        else:
            messages.error(request,"Invalid Login Or Password!!")
            
            return redirect('login1')
        
    return render(request, 'page-login1.html')

def doLogout(request):
    logout(request)
    return redirect("login")



def profile(request):
    current_user = request.user
    code = current_user.user_id
    rank = current_user.rank
   
    context = {
        'code': code,
        'rank':rank,
    }
    return render(request, 'profile.html',context)

def Profile_Update(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')


        try:
            customuser = CustomUser.objects.get(id = request.user.id)

            customuser.first_name = first_name
            customuser.last_name = last_name
            customuser.profile_pic = profile_pic
            if password != None and password !="":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Your Profile Updated Successfully !!")
            return HttpResponseRedirect(reverse("profile"))

            
            
        except :
            messages.error(request, "Failed to Update Your Profile")
            
        
    return render(request, 'HOD\profile.html')


def pendingPlot(request):
    return render(request,'HOD/pendingPlot.html')


def registeruser(request):
    
    current_user = request.user
    code = current_user.user_id
    rank = current_user.rank
   
    
    

    context = {
        'code':code,
        'rank':rank
        

    }

    return render(request,'register-user.html',context)

def registeruserr(request):


    return render(request,'register-userr.html')



def  cancelledplote(request):
    return render(request, 'HOD/cancelledplote.html')

def  blockassociatelist(request):
    return render(request, 'HOD/blockassociatelist.html')
def  tokenslip(request):
    return render(request, 'HOD/tokenslip.html')
def  pendingPlot(request):
    return render(request, 'HOD/pendingplot.html')
def  updatekyc(request):
    return render(request, 'HOD/updatekyc.html')

def  installmentdetail(request):
    Installment_data = BookCar.objects.all()
    context = {
        'Installment' : Installment_data
    }
    return render(request, 'HOD\installmentdetail.html', context)
def  supportsystem(request):
    return render(request, 'HOD/supportsystem.html')
def  userdashboard(request):
    return render(request, 'HOD/installmentdetail.html')




