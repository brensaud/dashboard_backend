from django.contrib.auth.models import Permission
from users.serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import exceptions, viewsets, status

from .authentication import generate_access_token, JWTAuthentication
from .serializers import PermissionSerializer, RoleSerializer, UserSerializer


from .models import Role, User

@api_view(['POST'])
def register(request):
    data = request.data

    if data['password'] != data['password_confirm']:
        raise exceptions.APIException('Password do not match')

    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


# @api_view(['GET'])
# def users(request):
#     serializer = UserSerializer(User.objects.all(), many=True)
#     return Response(serializer.data)



@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = User.objects.filter(email=email).first()

    if user is None:
        raise exceptions.AuthenticationFailed('User not found!')

    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('Incorrect Password!')
    

    response = Response()
    token = generate_access_token(user)
    response.set_cookie(key='jwt', value=token, httponly=True)

    response.data = {
        'jwt': token
    }
    return response



class AuthenticatedUser(APIView):
    authentication_classes = [JWTAuthentication]
    Permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user, many=True)

        return Response ({
            'data': serializer.data
        })


@api_view(['POST'])
def logout(request):
    response = Response()
    response.delete_cookie(key='jwt')
    response.data =  {
        'message': 'Success'
    }

    return response


class PermissionAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    Permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = PermissionSerializer(Permission.objects.all(), many=True)

        return Response ({
            'data': serializer.data
        })



class RoleViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    Permission_classes = [IsAuthenticated]

    def list(self, request):
        serializer = RoleSerializer(Role.objects.all(), many=True)

        return Response({
            'data': serializer.data
        })

    def create(self, request):
        serializer = RoleSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response({
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass 

    def destroy(self, request, pk=None):
        pass

