from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from ourcodeapi import views
from ourcodeapi.views import register_user, login_user, CategoryView, PostView, CoderView, ProjectView, EventView, AttendEvent, google_login, CommentView, fetch_latest_news, PostLiker, EventLiker
from rest_framework import routers


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', CategoryView, 'category')
router.register(r'posts', PostView, 'post')
router.register(r'coders', CoderView, 'coder')
router.register(r'projects', ProjectView, 'project')
router.register(r'events', EventView, 'event')
router.register(r'comments', CommentView, 'comment')

urlpatterns = [
    path('latest-news/', views.fetch_latest_news, name='latest-news'),
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('event/<int:event_id>/attend/', views.AttendEvent.as_view(), name='attend-event'),
    path('post/<int:post_id>/like/', views.PostLiker.as_view(), name='like-post'),
    path('event/<int:event_id>/like/', views.EventLiker.as_view(), name='like-event'),
    # path('google-login/', google_login, name='google-login'),
    path('auth/', include('social_django.urls', namespace='social')),
]

