import json
from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions, status, views, viewsets
from rest_framework.response import Response
from apps.authentication.models import UserAccount
from apps.authentication.permissions import IsAccountOwner
from apps.authentication.serializers import UserAccountSerializer

class UserAccountViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer

    def get_permission(self):
        if self.request.method in permissions.SAFE_METHOD:
            return (permissions.AllowAny(), )

        if self.request.method == 'POST':
            return (permissions.AllowAny(), )

        return (permissions.IsAuthenticated(), IsAccountOwner(), )

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            UserAccount.objects.create_user(**serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad Request',
            'message': 'Account cannot be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    def post(self, request, format=None):
        print "here"
        data = json.loads(request.body)
        email = data.get('email', None)
        password = data.get('password', None)
        account = authenticate(email=email, password=password)
        print account
        if account is not None:
            if account.is_active:
                login(request, account)
                serialized = UserAccountSerializer(account)
                return Response(serialized.data)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)

        return Response({}, status=status.HTTP_204_NO_CONTENT)
            
            


