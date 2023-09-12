from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from ourcodeapi.views import register_user, login_user, CategoryView, PostView
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', CategoryView, 'category')
router.register(r'posts', PostView, 'post')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]