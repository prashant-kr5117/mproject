from django.urls import path
from.import views
urlpatterns=[
    path('',views.index,name='index'),
    #path('bmipage/',views.bmipage,name='bmipage'),
    path('logininc/',views.logininc,name='logininc'),
    path('logininc/dashboard/',views.dashboard,name='dashboard'),
    path('logininc/dashboard/bmipage/',views.bmipage,name='bmipage'),
    path('signup/',views.signup,name='signup'),
    path('signup/adddetail/',views.adddetail,name='adddetail'),
    path('home/', views.home ,name = "/home"),
    path('result/', views.result ,name = "/result"),
]