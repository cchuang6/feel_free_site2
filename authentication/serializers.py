from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from authentication.models import Account


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Account
        read_only_fields = ('created_at', 'updated_at',)
        fields = (
            'email', 'businessname', 'spaceId', 'created_at',
            'updated_at', 'zipcode', 'city', 'state',
            'phone', 'tierlist', 'password', 'confirm_password',
            'is_staff', 'is_admin', 'is_superuser', 'is_active')

        def create(self, validated_data):
            return Account.objects.create(**validated_data)

        def update(self, instance, validated_data):
            instance.email = validated_data.get('email', instance.email)
            instance.businessname = validated_data.get('businessname',
                                                       instance.businessname)
            instance.zipcode = validated_data.get('zipcode', instance.zipcode)
            instance.city = validated_data.get('city', instance.city)
            instance.state = validated_data.get('state', instance.state)
            instance.phone = validated_data.get('phone', instance.phone)

            instance.save()

            password = validated_data.get('password', None)
            confirm_password = validated_data.get('confirm_password', None)

            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()

            update_session_auth_hash(self.context.get('request'), instance)

            return instance
