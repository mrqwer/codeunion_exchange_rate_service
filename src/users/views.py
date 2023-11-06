from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data.get('password')
        password2 = serializer.validated_data.get('password2')

        if password != password2:
            return Response({"error": "Passwords do not match."}, status=400)

        user = serializer.save()
        return Response({
            "user": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "message": "User created successfully.",
        })
