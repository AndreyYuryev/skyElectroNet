from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True}
        }
        read_only_fields = [
            'is_staff', 'is_superuser', 'is_active',
            # 'date_joined', 'last_login', 'groups', 'user_permissions',
        ]
