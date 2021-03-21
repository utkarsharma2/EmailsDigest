from rest_framework import serializers
from emailsdigest import models

class  ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Application
        fields = '__all__'


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Email
        fields = '__all__'