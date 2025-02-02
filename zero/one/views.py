from django.shortcuts import render, HttpResponse, redirect, reverse
import json
from django.contrib.auth.models import User
from .models import Customer, Extended
from django.contrib.auth import login,logout,authenticate,aauthenticate
from django.contrib.auth.decorators import login_required


class Student:
    def __init__(self, name, age, course, marks):
        self.name = name
        self.age = age
        self.course = course
        self.marks = marks


std_data = [
    {'name':'Ali','age':26, 'course':'django','marks':98},
    {'name':'Sahar','age':36,'course':'inter','marks':99},
    {'name':'Muskan','age':25,'course':'BS-SE','marks':90},
    {'name':'Anmol','age':27, 'course':'law','marks':88},
    {'name':'Ashir','age':20, 'course':'BA','marks':70},
    {'name':'Bilal','age':40, 'course':'MBA','marks':77},
]

student = []


def index(request):
    student = []
    for i in range(len(std_data)):
        std_obj = Student(std_data[i]['name'],std_data[i]['age'], std_data[i]['course'], std_data[i]['marks'])
        student.append(std_obj)
    return render(request,'index.html',{'std_data':student})


def data(request):
    if request.method == 'GET':
        obj = Customer.objects.all()
        return render(request,'home.html',{'cus_data':obj})
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer_obj = Customer(email=email, password=password)
        try:
            obj = Customer.objects.all()
            customer_obj.save()
            return render(request,'home.html',{'cus_data':obj})
        except:
            return HttpResponse('Data not saved')


def delete(request, id):
    obj = Customer.objects.get(pk=id)
    try:
        obj.delete()
        return redirect(reverse('data'))
    except:
        return HttpResponse('Data not found')


def update(request, id):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Fetch the existing object
            obj = Customer.objects.get(pk=id)

            # Update the fields
            obj.email = email
            obj.password = password

            # Save the updated object
            obj.save()

            # Redirect after successful update
            return redirect(reverse('data'))
        except Customer.DoesNotExist:
            return HttpResponse('Customer not found!')
        except Exception as e:
            return HttpResponse(f'Error: {e}')

    # Fetch the object to display in the update form
    obj = Customer.objects.get(pk=id)
    return render(request, 'update.html', {'cus': obj})


def mainpage(request):
    return render(request,'mainpage.html')


def mylogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Use 'username' instead of 'email'
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)  # Authenticate using username
        if user is not None:
            login(request, user)
            return render(request, 'admin_panel.html')  # Redirect to admin_panel.html on successful login
        else:
            return render(request, 'login.html', {'msg': 'Wrong Credentials'})  # Show error message
    if request.user.is_authenticated:
        return redirect(reverse('admin_panel'))
    else:
        return render(request, 'login.html')


@login_required(login_url='/mylogin/')
def admin_panel(request):
        return render(request,'login.html')


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        file = request.FILES['file']

        try:
            user = User.objects.create_user(username=username, email=email, password=password, is_active=True)
            e = Extended()
            e.id = user
            e.img = file
            e.save()
            return render(request,'signup.html',{'msg':'user created successfully!'})
        except:
            return render(request,'signup.html',{'msg':'user not created, Error'})
    return render(request,'signup.html')

def mylogout(request):
    logout(request)
    return render(request,'login.html')


from .serializers import CustomerSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET','POST'])
def cus_data(request):
    if request.method == 'GET':
        cus = Customer.objects.all()
        sr = CustomerSerializer(cus, many=True)
        return Response(sr.data)
    if request.method == 'POST':
        sr = CustomerSerializer(data=request.data)
        if sr.is_valid():
            sr.save()
            cus = Customer.objects.all()
            sr = CustomerSerializer(cus, many=True)
            return Response(sr.data)



