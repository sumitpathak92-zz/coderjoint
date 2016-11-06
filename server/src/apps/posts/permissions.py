from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication



@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated, ))
class IsAuthorOfPost(permissions.BasePermission):
    def has_object_permission(self, request, view, post):
        print "permission denied"
        if request.user:
            return post.author == request.user
        return False
