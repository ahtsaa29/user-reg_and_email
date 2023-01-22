from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from autheapp.serializers import EmployeeRegistrationSerializer , EmployeeLoginSerializer, EmployeeProfileSerializer, EmployeeChangePasswordSerializer, SendPasswordResetEmailSerializer, EmployeePasswordResetSerializer
from django.contrib.auth import authenticate
from autheapp.renderers import EmployeeRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated



def get_tokens_for_user(employee):
    refresh = RefreshToken.for_user(employee)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.
class EmployeeRegistrationView(APIView):
    renderer_classes = [EmployeeRenderer]
    def post(self, request,format=None):
        serializer = EmployeeRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        employee = serializer.save()
        token = get_tokens_for_user(employee)
        return Response({'token': token,'message':'registration success'}, status= status.HTTP_201_CREATED)



class EmployeeLoginView(APIView):
    renderer_classes = [EmployeeRenderer]
    def post(self, request,format=None):
        serializer = EmployeeLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token': token,'message':'login success'}, status= status.HTTP_201_CREATED)
        else:
            return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)



class EmployeeProfileView(APIView):
  renderer_classes = [EmployeeRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = EmployeeProfileSerializer(request.employee)
    return Response(serializer.data, status=status.HTTP_200_OK)



class EmployeeChangePasswordView(APIView):
  renderer_classes = [EmployeeRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = EmployeeChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'message':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
  renderer_classes = [EmployeeRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'message':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class EmployeePasswordResetView(APIView):
  renderer_classes = [EmployeeRenderer]
  def post(self, request, uid, token, format=None):
    serializer = EmployeePasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'message':'Password Reset Successfully'}, status=status.HTTP_200_OK)