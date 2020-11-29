from django.shortcuts import render
from .models import CustomUser
# Create your views here.
from django.contrib.auth import authenticate, login
from rest_framework import generics,permissions, status
from .serializers import CreateUserSerializer, LoginUserSerializer
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

class CreateUser(generics.GenericAPIView):

    serializer_class = CreateUserSerializer

    def post(self, request):
        user = self.request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()


        user_data = serializer.data
        user = authenticate(self.request, username=user['email'], password=user['password'])
        login(self.request, user)
        return redirect('home_page')


class LoginUser(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = LoginUserSerializer

    def post(self, request):
        user = self.request.data
        already_authenticated = self.request.user.is_authenticated

        if already_authenticated:
            return Response({"Already Logged In"}, status=status.HTTP_200_OK)


        incoming_email = user['email']
        incoming_password = user['password']
        serializer = self.serializer_class(data=user)

        user = authenticate(self.request, username=incoming_email, password=incoming_password)
        if user is not None:
            login(self.request, user)
            return redirect('home_page')
        return Response({"Unable to login"}, status=status.HTTP_401_UNAUTHORIZED)
