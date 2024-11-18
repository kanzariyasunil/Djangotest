from django.urls import path
from . import views
urlpatterns = [
    path('',views.blog,name = 'blogHome'),
    path('blogpost/<int:id>',views.blogpost,name = 'blogPost')
]


