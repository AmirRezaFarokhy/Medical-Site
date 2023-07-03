from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password 
from django.views.generic import ListView
from django.db.models import Q
from django.http import HttpResponse
from django.views import View 
from django.contrib import messages 

from rest_framework import generics
from api.serializers import SerializetionPatient 

from main.models import Doctor, PatientProfile


def validateCustomer(customer):
    error_message = None
    if (not customer.name):
        error_message = "Please Enter your First Name !!"
    elif len(customer.name) < 3:
        error_message = 'First Name must be 3 char long or more'
    elif not customer.last_name:
        error_message = 'Please Enter your Last Name'
    elif len(customer.last_name) < 3:
        error_message = 'Last Name must be 3 char long or more'
    elif len(customer.email) < 5:
        error_message = 'Email must be 5 char long'

    return error_message


class Login(View):

    return_url = None
    def get(self, request):
        Login.return_url = request.GET.get("return_url")
        return render(request=request, template_name='main/login.html')

    def post(self, request):
        name = request.POST.get("doctor")
        password = request.POST.get("password")
        doctor = Doctor.get_customers_by_name(name)
        print(doctor)
        error_message = None
        if doctor:
            if doctor.doctor==name and doctor.password==password:
                request.session['doctor'] = doctor.id
                return_url = None
                return redirect("main:homepage")
            else:
                error_message = 'Invalid !!'

        else:
            error_message = 'Invalid !!'

        print(name, password)
        return render(request=request, 
                      template_name="main/login.html", 
                      context={"error":error_message})


class Signup(View):

    def get(self, request):
        return render(request=request, 
                      template_name="main/signup.html")

    def post(self, request):
        postData = request.POST 
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }

        error_message = None
        customer = Doctor(firstname=first_name,
                             lastname=last_name,
                             phone=phone,
                             email=email,
                             password=password)

        error_message = validateCustomer(customer)
        print(error_message)
        if not error_message:
            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.save()
            return redirect('main:homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request=request, 
                          template_name='main/signup.html', 
                          context={"data":data})


class SearchView(ListView):
    model = PatientProfile
    template_name = "main/search_result.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = PatientProfile.objects.filter(
            Q(name__icontains=query),
            Q(last_name__icontains=query),
            Q(age__icontains=query),
            Q(email__icontains=query),
        )
        if object_list.exists():
            return object_list
        else:
            return messages.info(self.request, "Your data is't available...")


def logout(request):
    request.session.clear()
    return redirect('main:homepage')


def homepage(request):
    # this is a good thinking about it and great work...
    id_session = request.session.get('doctor')
    if id_session is not None:
        postdata = request.POST 
        name = postdata.get('name')
        lastname = postdata.get('lastname')
        age = postdata.get('age')
        description = postdata.get('description')
        email = postdata.get('email')

        values = {
            'name': name, 
            'last_name': lastname,
            'age': age,
            'description': description,
            'email': email
        }

        error_message = None
        patient = PatientProfile(name=name,
                                last_name=lastname,
                                age=age,
                                description=description,
                                email=email)
        error_message = validateCustomer(patient)
        print(error_message)

        if not error_message:
            print(values)
            patient.save()
            return redirect('main:homepage')

        doctor_profile_data = Doctor.objects.get(id=request.session['doctor'])

        doctor_profile_data
        return render(request, 
                    template_name='main/home.html',
                    context={'data':doctor_profile_data})

    return render(request, 
                  template_name='main/home.html') 



