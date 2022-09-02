from rest_framework import viewsets

from main.models import Status, Tag, Task, User
from main.serializers import (
    StatusSerializer,
    TagSerializer,
    TaskFilter,
    TaskSerializer,
    UserFilter,
    UserSerializer,
)


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
