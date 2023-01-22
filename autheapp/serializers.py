from rest_framework import serializers
from autheapp.models import Employee
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from autheapp.utils import Util



class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only = True)
    class Meta:
        model = Employee
        fields = ['email','name','password','password2','tc']
        extra_kwargs ={
            'password':{'write_only': True}
        }
    # validate pw
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError('Passwords do not match')
        # return super().validate(attrs)
        return attrs

    def create(self, validate_data):
        return Employee.objects.create_user(**validate_data)

class EmployeeLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = Employee
    fields = ['email', 'password']


class EmployeeProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Employee
    fields = ['id', 'email', 'name']


class EmployeeChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    user = self.context.get('user')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    user.set_password(password)
    user.save()
    return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if Employee.objects.filter(email=email).exists():
      employee = Employee.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(employee.id))
      print('Encoded UID', uid)
      token = PasswordResetTokenGenerator().make_token(employee)
      print('Password Reset Token', token)
      link = 'http://http://127.0.0.1:8000/api/user/reset/'+uid+'/'+token
      print('Password Reset Link', link)
      # Send EMail
      body = 'Click Following Link to Reset Your Password '+link
      data = {
        'subject':'Reset Your Password',
        'body':body,
        'to_email':employee.email
      }
      Util.send_email(data)
      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')

class EmployeePasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      employee = Employee.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(employee, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      employee.set_password(password)
      employee.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(employee, token)
      raise serializers.ValidationError('Token is not Valid or Expired')