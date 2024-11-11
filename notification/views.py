from rest_framework.views import APIView
from notification.serializers import CustomUserSerializer, NotificationSerializer
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Notification, CustomUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from .tasks import send_notification,test
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
import logging


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationViewset(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    

    def perform_create(self, request):
        logger = logging.getLogger(__name__)
        user = self.request.user
        serializer = NotificationSerializer(data=request.data)

        if serializer.is_valid():
            notification = serializer.save()

            scheduled_time = notification.scheduled_datetime
            current_time = timezone.localtime(timezone.now())
            print(f'{current_time} - {scheduled_time} = {scheduled_time - current_time} ')
            print(notification.notification_id)



            if scheduled_time > current_time:
                print('########## scheduled ##########')
                result = send_notification.apply_async(
                    kwargs={'notification_id': notification.notification_id}, eta=scheduled_time)
                logger.info(f"Task scheduled with id: {result.id}")
                return Response({'message': 'Notification scheduled successfully'}, status=status.HTTP_201_CREATED)

            else:
                result = send_notification.delay(notification.notification_id)
                logger.info(f"Task scheduled with id: {result.id}")

                return Response({'message': 'Notification sent successfully'}, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        username = self.request.user.pk
        notifications = Notification.objects.filter(user=username)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class login(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        username = request.data.get('username') or request.data.get('email')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Please provide both username/email and password'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = CustomUser.objects.filter(username=username).first() or CustomUser.objects.filter(email=username).first()

        if user is None:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return Response({'message': 'Login successful',
                         'access': str(refresh.access_token),
                         'refresh': str(refresh)                         
                         }, status=status.HTTP_200_OK)


def register_view(request):
    return render(request,'notification/reg.html')

def login_view(request):
    return render(request,'notification/login.html')

def dashboard(request):
    return render(request,'notification/idx.html')