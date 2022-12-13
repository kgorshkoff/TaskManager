from typing import cast

from rest_framework import viewsets

from main.models import Status, Tag, Task, User
from main.serializers import (
    CurrentUserSerializer, StatusSerializer,
    TagSerializer,
    TaskFilter,
    TaskSerializer,
    UserFilter,
    UserSerializer,
)
from main.services.single_resource import SingleResourceMixin, SingleResourceUpdateMixin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.prefetch_related("tags")
    serializer_class = TaskSerializer
    filterset_class = TaskFilter


class CurrentUserViewSet(
    SingleResourceMixin, SingleResourceUpdateMixin, viewsets.ModelViewSet
):
    serializer_class = CurrentUserSerializer
    queryset = User.objects.order_by("id")

    def get_object(self) -> User:
        return cast(User, self.request.user)
