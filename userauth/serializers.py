import json
from rest_framework import serializers
from .models import User, UserProfile
from django.contrib.auth import authenticate
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from userauth.models import User, OtpModel
from rest_framework import exceptions
from userauth import views 
from django.conf import settings
import urllib.request

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        request = self.context["request"].data
        data = json.dumps(request)
        request_data = json.loads(data)

        email = request_data.get("email","")
        password = request_data.get("password","")
        try:
            user = User.objects.get(email__iexact = email)
        except:
            raise exceptions.ParseError("User with entered email doesn't exists.")   #400
        if user.is_active:
            if user.check_password(password):
                data = super(MyTokenObtainPairSerializer, self).validate(attrs)
                data.update({'email': self.user.email})
                data.update({'name' : self.user.profile.name})
                try:
                    domain_name = self.context["request"].META['HTTP_HOST']
                    picture_url = self.user.profile.picture.url
                    absolute_url = 'http://' + domain_name + picture_url
                    data.update({'picture': absolute_url})
                except:
                    data.update({'picture': None})
                return data                                                          #200
            raise exceptions.AuthenticationFailed("Entered password is wrong")       #401
        views.send_otp_email(email, body = "Hello Your OTP for verifying your account")
        raise exceptions.PermissionDenied("User is registered but not verified")     #403


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = UserProfile
        fields = ('id','name','blood_grp','picture','address','city','state','phone','covid_patient','recovered','got_help','when_recovered','want_to_donate','can_donate','available_as_donor','needs_help')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=True)
    class Meta:
        model = User
        fields = ('id','email','password', 'profile',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user,**profile_data)
        return user

    def update(self, instance, validated_data):
        try:
            profile_data = validated_data.pop('profile')
            profile = instance.profile
            UserProfileSerializer(instance.profile).update(instance=instance.profile,validated_data=profile_data)
        except:
            pass
        instance.email = validated_data.get('email', instance.email)
        try:
            new_password = validated_data['password']
            instance.set_password(new_password)
        except:
            pass
        instance.save()
        return instance
