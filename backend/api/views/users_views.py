from api.pagination import LimitPageNumberPagination
from api.serializers.users_serializers import SubscriptionsSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Follow, User


class ListSubscriptions(viewsets.ModelViewSet):
    serializer_class = SubscriptionsSerializer
    pagination_class = LimitPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.filter(following__user=user)
        return queryset


class Subscribe(APIView):
    def delete(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        if not (
            user == author or Follow.objects.filter(user=user,
                                                    author=author).exists()
        ):
            return Response(
                {"errors": "Subscription not available"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        subscription = get_object_or_404(Follow, user=user, author=author)
        subscription.delete()
        return Response(
            {"errors": "Successful resubscription"},
            status=status.HTTP_204_NO_CONTENT
        )

    def post(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author or Follow.objects.filter(user=user,
                                                   author=author).exists():
            return Response(
                {
                    "errors": "Subscription not available "
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        Follow.objects.get_or_create(user=user, author=author)
        serializer = SubscriptionsSerializer(author,
                                             context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
