from django.contrib.auth import get_user_model, authenticate
# outputting message into output screen
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializers for the users object"""

    class Meta:
        model = get_user_model()
        # fields when creating a new user
        fields = ('email', 'password', 'name')
        # restrictions or arguments for the password mentioned above
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}


    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        # take password out of the data to encrypt it
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    # validate serializer, checking inputs are correct
    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
