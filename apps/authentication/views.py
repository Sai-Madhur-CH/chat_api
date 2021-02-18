from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from .serializer import RegisterSerializer, LoginSerializer


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
