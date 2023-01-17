from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("donors_list/<int:myid>/", views.donors_list, name="donors_list"),
    path("allcountry", views.allcountry, name="allcountry"),
    path("city_list/<int:myid>/", views.city_list, name="city_list"),
    path("vanue_list/<int:myid>/", views.vanue_list, name="vanue_list"),

    path("donors_dedend/<int:myid>/", views.donors_dedend, name="donors_dedend"),
    path("donors_details/<int:myid>/", views.donors_details, name="donors_details"),
   

    path("request_blood/", views.request_blood, name="request_blood"),
    path("see_all_request/", views.see_all_request, name="see_all_request"),
    # path("become_donor/", views.become_donor, name="become_donor"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_status/', views.change_status, name='change_status'),
    path('forgetpassword' , views.forgetpassword, name="forgetpassword"),
    path('change-password/<token>/' , views.ChangePassword , name="change_password"),
    path('contact',views.contact,name="contact"),

    
    #  path('get-topics-ajax/', views.get_topics_ajax, name="get_topics_ajax"),
    path('become_donor/', views.signup_view, name='become_donor'),

    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('ajax/load-vanues/', views.load_vanues, name='ajax_load_vanues'),


]