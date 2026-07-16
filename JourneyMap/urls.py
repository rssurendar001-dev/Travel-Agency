from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.home, name='home'),
    
    path('about/', views.about, name='about'),
    
    path('contact/', views.contact, name='contact'),
    
    path('packages/', views.packages, name='packages'),
    
    path('destinations/<str:category>/',views.destinations,name='destinations'),
    
    path("enquiry/<int:destination_id>/",views.enquiry,name="enquiry"),
    
    path("blog/",views.blog,name="blog"),
    
    path("travel-goal/",views.travel_goal,name="travel_goal"),
    
    path('budget-planner/', views.budget_planner, name='budget_planner'),
    
    path('login/', views.user_login, name='login'),
    
    path('signup/', views.signup, name='signup'),
    
    path('logout/', views.user_logout, name='logout'),
    
    path('travel-cost/',views.travel_cost,name='travel_cost'),
    
    path('travel-buddy/',views.travel_buddy,name='travel_buddy'),
    
    path('currency-converter/',views.currency_converter,name='currency_converter'),
    
    path("verify-otp/",views.verify_otp,name="verify_otp"),
    
]