from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .models import User
from .serializers import UserSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter


class UserRegistrationView(APIView):
    """
    Handles user registration
    """

    @extend_schema(
        request=UserSerializer,
        responses={201: UserSerializer, 400: "Bad Request"},
        description="Register a new user with a unique username and initial balance.",
        summary="Register User",
        methods=["POST"]
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .models import User
from .serializers import UserSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter

class UserDetailView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter("username", description="Username of the user", required=True, type=str, location=OpenApiParameter.PATH)
        ],
        responses={200: UserSerializer, 404: {"error": "User not found"}},
        description="Retrieve a user's details by their username. Cached for 5 minutes.",
        summary="Retrieve User by Username",
        methods=["GET"]
    )
    def get(self, request, username):
        cached_user = cache.get(f"user_{username}")
        if cached_user:
            return Response(cached_user, status=status.HTTP_200_OK)

        try:
            user = User.objects.get(username=username)
            serializer = UserSerializer(user)
            cache.set(f"user_{username}", serializer.data, timeout=300)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

