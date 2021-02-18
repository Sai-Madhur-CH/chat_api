from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from .serializer import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User


class RegisterUser(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.data)
            return Response(data={'status': 'success'}, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            response = serializer.auth(serializer.data)
            if response.get('status') == 'success':
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                return Response(data=response, status=status.HTTP_401_UNAUTHORIZED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = User.objects.all().values('id',
                                             'username', 'email', 'first_name', 'last_name')
        return Response(data=queryset, status=status.HTTP_200_OK)
