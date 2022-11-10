from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, generics, permissions, viewsets
from complaintApp.models import UserMaster, ComplaintMaster
from complaintApp.serializers import *
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters


class LoginViewSet(mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = UserMaster.objects.all()
    serializer_class = UserMasterSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        if email is None or password is None:
            return Response({'errors': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=email, password=password)
        if not user:
            return Response({'errors': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        token, created = Token.objects.get_or_create(user=user)
        data = {
            'X-Token': token.key,
            'user_id': user.id
        }
        return Response(data=data, status=status.HTTP_200_OK)


class LogoutViewSet(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_200_OK)


class RegistrationViewSet(mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = UserMaster.objects.all().order_by('-id')
    serializer_class = UserMasterSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        if email is None or password is None:
            return Response({'errors': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
        check_exist = UserMaster.objects.filter(email=email).exists()
        if check_exist:
            return Response({'errors': 'already exist.'}, status=status.HTTP_400_BAD_REQUEST)
        UserMaster.objects.create(email=email, custom_password=password)
        return Response(status=status.HTTP_200_OK)


class UserComplaintViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    queryset = ComplaintMaster.objects.all().order_by('-id')
    serializer_class = ComplaintMasterSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ['status']

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(created_by=user)
    
    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.id
        serializer = ComplaintMasterSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        request.data['created_by'] = request.user.id
        serializer = ComplaintMasterSerializer(obj, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkerComplaintViewSet(mixins.ListModelMixin,
                           mixins.UpdateModelMixin,
                           viewsets.GenericViewSet):
    queryset = ComplaintMaster.objects.all().order_by('-id')
    serializer_class = ComplaintMasterSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ['status']

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        request.data['updated_by'] = request.user.id
        serializer = ComplaintMasterSerializer(obj, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
