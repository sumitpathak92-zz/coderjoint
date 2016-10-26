from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from authentication.models import UserAccount

class UserAccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model=Account
        fields = ('id', 'email', 'username', 'joined_on', 'profile_last_updated', 
                 'first_name', 'last_name', 'password', 'confirm_password'
                 'about_me', 'status', 'exp_type',)
        read_only_fields = ('joined_on', 'profile_last_updated', )
        
        def create(self, validated_data):
            return UserAccount.objects.create(**validated_data)

        def update(self, instance, validated_data):
            instance.username = validated_data.get('username', instance.username)
            instance.about_me = validated_data.get('about_me', instance.about_me)
            instance.status = validated_data.get('status', instance.status)

            instance.save()
            password = validated_data.get('password', None)
            confirm_password = validated_data.get('confirm_password', None)

            if password and confirm_password and password==confirm_password:
                instance.set_password(password)
                instance.save()

            update_session_auth_hash(self.context.get('request'), instance)

            return instance

