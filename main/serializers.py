from rest_framework import serializers
from django.contrib.auth.models import User

# Create your views here.
class RegistrationSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password == password2:
            user = User.objects.create(
                username = self.validated_data['username'],
                email = self.validated_data['email'],
            )
            user.set_password(password)
            user.save()
            return user
        raise serializers.ValidationError({'password': 'passwords do not match!'})