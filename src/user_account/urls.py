from django.urls import path
from django.views.generic import TemplateView

from user_account.views import CreateUserAccountView, UserAccountLoginView, UserAccountLogoutView, \
    UserAccountUpdateView

urlpatterns = [
    path('register/success', TemplateView.as_view(template_name='success.html'), name='success'),
    path('register/', CreateUserAccountView.as_view(), name='registration'),
    path('login/', UserAccountLoginView.as_view(), name='login'),
    path('logout/', UserAccountLogoutView.as_view(), name='logout'),
    path('profile/', UserAccountUpdateView.as_view(), name='profile'),


]
