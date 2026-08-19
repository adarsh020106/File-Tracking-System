from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *


# Create your views here.
def admindash(request):
    if 'adminid' not in request.session:
        messages.error(request, "Please login first")
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    file_count = File.objects.all().count()
    pending_file = File.objects.filter(status="OPEN").count()
    total_dpt=Department.objects.filter(is_active=True).count()
    total_emp=Employee.objects.filter(is_active=True).count()
    context = {
        'adminid' : adminid,
        'file_count':file_count,
        'total_dpt':total_dpt,
        'total_emp':total_emp,

    }
    return render(request, "admindash.html", context)

def adminlogout(request):
    if 'adminid' not in request.session:
        del request.session['adminid']
        messages.success(request, "Logged out Successfully")
        return redirect('adminlogin')
    else:
        return redirect('adminlogin')
    
def adddept(request):
    if 'adminid' not in request.session:
        messages.error(request, "Please login first")
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    context = {
        'adminid' : adminid,
    }
    if request.method == "POST":
        dept_name = request.POST.get('dept_name')
        if Department.objects.filter(dept_name=dept_name):
            messages.warning(request,"This department already exits")
            return redirect("adddept")
        dep=Department(dept_name= dept_name)
        dep.save()
        messages.success(request,"Department added successfully")
        return redirect("viewdept")
    return render(request, "adddept.html", context)    



def viewdept(request):
    if 'adminid' not in request.session:
        messages.error(request, "Please login first")
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    depts= Department.objects.filter(is_active=True)
    context = {
        'adminid' : adminid,
        'depts' : depts,
    }
    return render(request, "viewdept.html", context)    

def viewemp(request):
    if 'adminid' not in request.session:
        messages.error(request, "Please login first")
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    depts = Department.objects.filter(is_active=True)
    emp1 = Employee.objects.filter(is_active=True)
    context = {
        'adminid' : adminid,
        'depts' : depts,
        'emp1' : emp1,

    }
    return render(request, "viewemp.html", context)   



 
def addemp(request):
    if 'adminid' not in request.session:
        messages.error(request, "Please login first")
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    depts= Department.objects.filter(is_active=True)

    context = {
        'adminid' : adminid,
        'depts' : depts,
    }
    if request.method == "POST":
        empid = request.POST.get('empid')
        name = request.POST.get('name')
        email = request.POST.get('email')
        contactno = request.POST.get('contactno')
        designation= request.POST.get('designation')
        dept_id= request.POST.get('dept_id')
        dept = Department.objects.get(id=dept_id)
        if LoginInfo.objects.filter(username=email):
            messages.warning(request,"This email alredy registered")
            return redirect("addemp")
        log =LoginInfo.objects.create(usertype='employee',username=email,password="12345678",)
        emp=Employee.objects.create(log=log,empid=empid,name=name,email=email,contactno=contactno, designation= designation,department=dept)
        messages.success(request, "Employee added successfully")
        return redirect("viewemp")
    return render(request, "addemp.html", context)    


def changepass(request):
    if 'adminid' not in request.session:
        messages.error(request, "Please login first")
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    context = {
        'adminid' : adminid,
    }
    if request.method == "POST":
        oldpwd = request.POST.get("oldpwd")
        newpwd = request.POST.get("newpwd")
        cnfpwd = request.POST.get("cnfpwd")
        admin = LoginInfo.objects.get(username=adminid)
        if newpwd != cnfpwd:
         messages.warning(request, "Enter same passward")
         return redirect("changepass")
        if oldpwd !=admin.password:
            messages.error(request,"old passward is incorrect")
            return redirect("changepass")
        if newpwd == admin.password:
            messages.warning(request, "You cannot set Perious Password ")
            return redirect("changepass")
        admin.password = newpwd
        admin.save()
        messages.success(request,"Password chnage successfully")
        return redirect("changepass")
    return render(request, "changepass.html", context) 

def deldept(request,did):
    if 'adminid' not in request.session:
        messages.error(request,"Please Login first")
        return redirect ('adminlogin')
    if  Department.objects.filter(id=did):
        dept=Department.objects.get(id=did)
        dept.is_active=False
        dept.save()
        messages.success(request, "Department deleted successfully")
        return redirect("viewdept")
           
    else:
        return redirect("viewdept")
   



def allfiles(request):
    if 'adminid' not in request.session:
        messages.error(request, "Please login first")
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    files = File.objects.all()
    context = {
        'adminid' : adminid,
        'files':files,
    }
    return render(request, "allfiles.html", context)    

def delemp(request,did):
    if 'adminid' not in request.session:
        messages.error(request,"Please Login first")
        return redirect ('adminlogin')
    if  Employee.objects.filter(id=did):
        emp=Employee.objects.get(id=did)
        emp.is_active=False
        LoginInfo.objects.filter(employee=emp).update(is_active=False)
        emp.save()
      
        messages.success(request, "Employee deleted successfully")
        return redirect("viewemp")
           
    else:
        return redirect("viewemp")