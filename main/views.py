from typing import cast, Any

from django.http import Http404, HttpResponse
from django.urls import reverse
from rest_framework import viewsets, mixins, status
from rest_framework.request import Request
from rest_framework.response import Response

from main.models import Status, Tag, Task, User
from main.serializers import (
    CurrentUserSerializer,
    StatusSerializer,
    TagSerializer,
    TaskFilter,
    TaskSerializer,
    UserFilter,
    UserSerializer,
    CountdownJobSerializer, JobSerializer,
)
from main.services.async_celery import AsyncJob, JobStatus
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


class CountdownJobViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CountdownJobSerializer

    def get_success_headers(self, data: dict) -> dict[str, str]:
        task_id = data["task_id"]
        return {"Location": reverse("jobs-detail", args=[task_id])}


class AsyncJobViewSet(viewsets.GenericViewSet):
    serializer_class = JobSerializer

    def get_object(self) -> AsyncJob:
        lookup_url_kwargs = self.lookup_url_kwarg or self.lookup_field
        task_id = self.kwargs[lookup_url_kwargs]
        job = AsyncJob.from_id(task_id)
        if job.status == JobStatus.UNKNOWN:
            raise Http404()
        return job

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponse:
        instance = self.get_object()
        serializer_data = self.get_serializer(instance).data
        if instance.status == JobStatus.SUCCESS:
            location = self.request.build_absolute_uri(instance.result)
            return Response(
                serializer_data,
                headers={"location": location},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer_data)
