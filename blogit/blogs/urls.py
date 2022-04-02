from django.urls import path

from .views import BlogUpdate, BlogsList, GetUserInformation, LikesCreate

urlpatterns = [
    path(r'', BlogsList.as_view()),
    path('<int:pk>', BlogUpdate.as_view()),
    path('users', GetUserInformation.as_view()),
    path('<int:pk>/like', LikesCreate.as_view()),

]
