from django.contrib import admin
from django.urls import path, include
from crud import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('authentication.urls')),
    path('api/user/', include('dashboard.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('crud.urls')),

]
