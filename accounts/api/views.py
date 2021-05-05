from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from accounts.api.serializers import RegisterUserSerializer


class RegisterAPIView(APIView):
    """
    API View that registers the user and returns Auth Token.
    """

    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if not serializer.is_valid():
            return Response(data={**serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # Token is created in def create() in serializer_class and returned

        token = serializer.save()

        return Response(data={'token': str(token)}, status=status.HTTP_201_CREATED)


LoginAPIView = ObtainAuthToken
