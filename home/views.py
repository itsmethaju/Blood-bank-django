
from django.contrib import messages
from django.urls import reverse

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from . models import *
from . forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .helpers import send_forget_password_mail,send_contact_mail
import uuid
from urllib import request

def index(request):
    all_group = BloodGroup.objects.annotate(total=Count('donor'))
    user = User.objects.all().count()
    req = RequestBlood.objects.all().count()
    return render(request, "home.html", {'all_group':all_group,'user':user,'req':req})

def donors_list(request, myid):
    blood_groups = BloodGroup.objects.filter(id=myid).first()
    donor = Donor.objects.filter(blood_group=blood_groups)
    return render(request, "donerslist.html", {'donor':donor})

def donors_details(request, myid):
    details = Donor.objects.filter(id=myid)[0]
    return render(request, "donerdlt.html", {'details':details})
##########################################################################
def allcountry(request):
    all_Country = State.objects.annotate(total=Count('donor'))
  
    return render(request, "country.html",{'all_group':all_Country,})
def city_list(request, myid):
    state = State.objects.filter(id=myid).first()
    city = District.objects.filter(state=state)
    return render(request, "city.html", {'city':city})

def vanue_list(request, myid):
    district = District.objects.filter(id=myid).first()
    vanue = City.objects.filter(district=district)
    return render(request, "vanue.html", {'vanue':vanue})

def donors_dedend(request, myid):
    city = City.objects.filter(id=myid).first()
    donor = Donor.objects.filter(city=city)
    return render(request, "donersfinellist.html", {'donor':donor})
###################################################################################
def request_blood(request):

    if request.method == 'POST':
        form = RequestBloodForm(request.POST)
       

        if form.is_valid() :
  
            form.save()
            messages.success(request, 'Your Blood Request successfully')
            return redirect('/')
    else:
        state =State.objects.all()
        bloodgroup=BloodGroup.objects.all()
        form = RequestBloodForm()
    return render(request, "reqblood.html",{"form":form,'state':state,'bloodgroup':bloodgroup})

def see_all_request(request):
    requests = RequestBlood.objects.all()
    return render(request, "allreq.html", {'requests':requests})

def become_donor(request):
    if request.method=="POST":   
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        state = request.POST['state']
        city = request.POST['city']
        panjayath=request.Post['panjayath']
        address = request.POST['address']
        gender = request.POST['gender']
        blood_group = request.POST['blood_group']
        date = request.POST['date']
        image = request.FILES['image']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('/signup')

        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
        donors = Donor.objects.create(donor=user, phone=phone, state=state, city=city,blockpanchayaths=panjayath, address=address, gender=gender, blood_group=BloodGroup.objects.get(name=blood_group), date_of_birth=date, image=image)
        user.save()
        donors.save()
        profile_obj = Profile.objects.create(user=user)
        profile_obj.save()
        return render(request, "index.html")
    states = State.objects.all()
    city1 = City.objects.all()
    street = Street.objects.all()
    return render(request, "doner-reg.html",{'state':states,'city':city1,'street':street})


def Login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("/profile")
            else:
                thank = True
                donor_profile = Donor.objects.get(donor=request.user)
                return render(request, "profile.html", {'donor_profile':donor_profile})
    return render(request, "login.html")

def Logout(request):
    logout(request)
    return redirect('/')

@login_required(login_url = '/login')
def profile(request):
    donor_profile = Donor.objects.get(donor=request.user)
    return render(request, "profile.html", {'donor_profile':donor_profile})

@login_required(login_url = '/login')
def edit_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.donor)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('profile')
    else:
     
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.donor)
        donor_profile = Donor.objects.get(donor=request.user)
    return render(request, 'profile-edit.html', {'user_form': user_form, 'profile_form': profile_form,'donor_profile':donor_profile})
    # return render(request, "profile-edit.html", {'donor_profile':donor_profile})

@login_required(login_url = '/login')
def change_status(request):
    donor_profile = Donor.objects.get(donor=request.user)
    if donor_profile.ready_to_donate:
        donor_profile.ready_to_donate = False
        donor_profile.save()
    else:
        donor_profile.ready_to_donate = True
        donor_profile.save()
    return redirect('/profile')


def ChangePassword(request, token):
    context = {}

    try:
        profile_obj = Profile.objects.filter(
            forget_password_token=token).first()
        context = {'user_id': profile_obj.user.id}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')

            if new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password/{token}/')

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('login')

    except Exception as e:
        print(e)
    return render(request, 'change-password.html', context)


def forgetpassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not User.objects.filter(username=username).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('forgetpassword')

            user_obj = User.objects.get(username=username)
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.get(user=user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email, token)
            messages.success(request, 'An email is sent. Check Your Email')
            return redirect('forgetpassword')

    except Exception as e:
        print(e)
    return render(request, 'forget-password.html')






from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from .forms import PersonForm,UserForm


class PersonListView(ListView):
    model = Person
    context_object_name = 'people'
from django.http import HttpResponseRedirect

def signup_view(request):
    userForm=UserForm()
    doctorForm=PersonForm()
    state =State.objects.all()
    bloodgroup=BloodGroup.objects.all()
    mydict={'userForm':userForm,'doctorForm':doctorForm,'state':state,'bloodgroup':bloodgroup}
    if request.method=='POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
   
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('become_donor')
        elif User.objects.filter(username=username).exists():
                messages.info(request,'User Name Already Created')
                return redirect('become_donor')
        elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Already Exist')
                return redirect('become_donor')
           
        userForm=UserForm(request.POST)
        doctorForm=PersonForm(request.POST,request.FILES)
        
        if userForm.is_valid() and doctorForm.is_valid():
            user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
  
 
            user.save()
            donor=doctorForm.save(commit=False)
            donor.donor=user
            donor=donor.save()
        
            profile_obj = Profile.objects.create(user=user)
            profile_obj.save()
            messages.info(request,'Sucess....')
        return redirect('login')
       
    return render(request,'home/person_form.html',context=mydict)






def load_cities(request):
    state_id = request.GET.get('state')    
    district = District.objects.filter(state_id=state_id).order_by('name')
    context = {'cities': district}
    return render(request, 'city_dropdown_list_options.html', context)

def load_vanues(request):
    district_id = request.GET.get('district')    
    city = City.objects.filter(district_id=district_id).order_by('name')
    context = {'vanues': city}
    print(city)
    return render(request, 'vanue_ddl.html', context)



def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        contact =Contact.objects.create(name=name,email=email,message=message)
        contact.save()
        send_contact_mail(name,email,message)
    
    return redirect('/')

