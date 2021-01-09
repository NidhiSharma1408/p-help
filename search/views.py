from django.http import Http404
from django.utils import timezone
from django.shortcuts import render
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny,IsAuthenticated
from userauth.models import UserProfile
from . import serializers,models
from .permissions import IsSender,IsReceiver


class SearchView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if 'city' in request.GET:
            queryset = UserProfile.objects.filter(city__icontains=request.GET['city']).exclude(user=request.user)
        if 'blood_grp' in request.GET:
            queryset = UserProfile.objects.filter(blood_grp__icontains=request.GET['blood_grp']).exclude(user=request.user)
        response = []
        for user in queryset:
            if user.available_as_donor():
                response.append({'id':user.id,'name':user.name,'email':user.user.email,'phone':user.phone, 'address' :f"{user.address}, {user.city}, {user.state}"})
        return Response(response[:50])


class RequestModelViewset(ModelViewSet):
    model = models.DonationRequest
    queryset = models.DonationRequest.objects.all()
    serializer_class = serializers.RequestSerializer
    def get_queryset(self):
        return models.DonationRequest.objects.filter(receiver=self.request.user.profile)|models.DonationRequest.objects.filter(sender=self.request.user.profile)

    def create(self,request,format=None):
        data=request.data
        if 'receiver' in data:
            receiver = data['receiver']
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if receiver == request.user.profile.id:
            return Response({"detail" : "Can't send request to yourself."},status=status.HTTP_400_BAD_REQUEST)
        data['sender'] = request.user.profile.id
        try:
            receiver = UserProfile.objects.get(id=receiver)
        except:
            return Response({"detail": "User does not exist or is not available as a donor."},status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        request.data['accepted'] = True
        models.DonationRequest.objects.filter(receiver=request.user.profile.id).exclude(id=self.get_object().id).delete()
        models.DonationRequest.objects.filter(sender=self.get_object().sender.id).exclude(id=self.get_object().id).delete()
        return self.update(request, *args, **kwargs)

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif self.action == 'partial_update':
            permission_classes = [IsReceiver]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]  


class DonationHistoryView(ModelViewSet):
    model = models.DonationHistory
    serializer_class = serializers.DonationHistorySerializer
    queryset = models.DonationHistory.objects.all()
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return models.DonationHistory.objects.filter(donated_by=self.request.user.profile)

    def create(self,request,format=None):
        if 'id' in request.data:
            receiver = data['id']
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            donation_request=models.DonationRequest.objects.get(id=id,accepted=True,receiver=request.user.id)
        except:
            return Response({"detail" : "No such donation request found."}, status=status.HTTP_400_BAD_REQUEST)
        data={}
        data['donated_by'] = request.user.profile.id
        data['donated_to'] = donation_request.sender.id
        data['donated_on'] = request.data.get('donated_on',timezone.now.date()) 
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
