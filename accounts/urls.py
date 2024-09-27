from django.urls import path
from .views import home_view, login_view, register_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('accounts/login/', login_view, name='login'),
    path('', register_view, name='register'),
    path('home/', home_view, name='home'),  
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
