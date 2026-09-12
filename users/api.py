from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from .models import Profile
from .serializers import ProfileSerializer


@extend_schema(
    tags=['Users'],
    summary='Мой профиль',
    description='Профиль текущего авторизованного пользователя.',
)
class MyProfileAPIView(generics.RetrieveAPIView):
    """GET /api/profile/me/ — мой профиль (только для авторизованных)."""
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile