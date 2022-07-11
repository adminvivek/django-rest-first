from unicodedata import name
from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'todo-view-set', TodoViewSet, basename='todo')

urlpatterns = [
    path('', get_api , name='get_api'),
    path('get-todo/', get_todo, name='get_todo'),
    path('post-todo/', post_todo, name='post_todo'),
    path('patch-todo/', patch_todo, name="patch_todo"),


    path('todo/', TodoView.as_view()),
]

urlpatterns += router.urls