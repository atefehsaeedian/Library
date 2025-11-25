from django.shortcuts import redirect, render
from rest_framework.views import  APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import login, logout
from django.contrib import messages
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):
    permission_classes = [AllowAny]
    template_name = 'accounts/register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            messages.success(request, 'Account created! Please log in.')
            return redirect('accounts:login')
        return render(request, self.template_name, {'errors': serializer.errors})

class LoginView(APIView):
    permission_classes = [AllowAny]
    template_name = 'accounts/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('books:book_list')

        messages.error(request, 'Invalid username or password.')
        return render(request, self.template_name)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        messages.info(request, 'You have been logged out.', 'info')
        return redirect('books:book_list')

