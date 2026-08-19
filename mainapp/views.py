from django.shortcuts import render,redirect
from.models import LoginInfo
from django.contrib import messages


# Create your views here.
def index(request):
        return render(request, "index.html")
def contact(request):
        return render(request, "contact.html")
def adminlogin(request):
        if request.method == "POST":
                username = request.POST.get('username')
                password = request.POST.get('password')
                try:
                        admin=LoginInfo.objects.get(username=username,password=password,usertype="admin",is_active=True)
                        if admin.is_active:
                                messages.success(request, "Welcome Admin")
                                request.session['adminid']=admin.username
                                return redirect('admindash')
                        pass
                except LoginInfo.DoesNotExist:
                        messages.warning(request, "Invailid username or password")
                        return redirect('adminlogin')
        return render(request, "adminlogin.html")

def userlogin(request):
        if request.method == "POST":
                        username = request.POST.get('username')
                        password = request.POST.get('password')
                        try:
                                emp=LoginInfo.objects.get(username=username,password=password,usertype="employee", is_active=True)
                                if emp.is_active:
                                        messages.success(request, "Welcome Employee")
                                        request.session['eid']=emp.username
                                        return redirect('empdash')
                                
                        except LoginInfo.DoesNotExist:
                                messages.warning(request, "Invailid username or password")
                                return redirect('userlogin')
        return render(request, "userlogin.html")

 