from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from . serializers import FarmerRegistrationSerializer,FarmerLoginSerializer,FarmerProfileSerializer,FarmerChangePasswordSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from . renderers import FarmerRenderer
from rest_framework.permissions import IsAuthenticated

#generate tokan manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class FarmerRegistrationView(APIView):
    renderer_classes = [FarmerRenderer]
    def post(self, request,format = None):
        serializer = FarmerRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            Farmer = serializer.save()
            token = get_tokens_for_user(Farmer)
            return Response({'token':token,'msg':'Registration Successful'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class FarmerLoginView(APIView):
    renderer_classes = [FarmerRenderer]
    def post(self,request,format = None):
        serializer = FarmerLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            Farmer = authenticate(email=email, password=password)
            if Farmer is not None:
                token = get_tokens_for_user(Farmer)
                return Response({'token':token,'msg':'Login Successful'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
            

class FarmerProfileView(APIView):
  renderer_classes = [FarmerRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = FarmerProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


class FarmerChangePasswordView(APIView):
  renderer_classes = [FarmerRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = FarmerChangePasswordSerializer(data=request.data, context={'Farmer':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
  renderer_classes = [FarmerRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  renderer_classes = [FarmerRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)