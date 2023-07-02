from django.urls import path

from main.views import (
            Login, Signup, 
            logout, homepage
        )

urlpatterns = [
    path('', homepage, name='homepage'),
    path('login', Login.as_view(), name='login'),
    path('signup', Signup.as_view(), name='signup'),
    path('logout', logout, name='logout'),
]

