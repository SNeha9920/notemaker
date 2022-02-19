from rest_framework import serializers
from .models import *

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        db_table: 'user_login'
        model = Signup
        abstract =True
        fields = '__all__'

class JournalsSerializer(serializers.ModelSerializer):
    class Meta:
        db_table: 'journals'
        model = Journals
        abstract =True
        fields = '__all__'

class PagesSerializer(serializers.ModelSerializer):
    class Meta:
        db_table: 'pages'
        model = Pages
        abstract =True
        fields = '__all__'

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        db_table: 'images'
        model = Images
        abstract =True
        fields = '__all__'