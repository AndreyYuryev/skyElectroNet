from rest_framework import viewsets
from users.models import User
from users.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.permissions import IsCurrentUser


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated, ]
        elif self.action == 'create':
            permission_classes = [IsAdminUser, ]
        else:
            permission_classes = [IsAuthenticated, IsCurrentUser | IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()

    def perform_update(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()
