from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'registration'

urlpatterns = [
    path('sign-up/', views.sign_up, name='sign_up'),
    path('sign-in/', views.LoginCustom.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset', views.PasswordResetViewCustom.as_view(), name='password_reset'),
    path('password-reset/done', views.PasswordResetDoneViewCustom.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>', views.PasswordResetConfirmViewCustom.as_view(), name='password_reset_confirm'),
    path('password-reset/complete', views.PasswordResetCompleteViewCustom.as_view(), name='password_reset_complete'),
]
