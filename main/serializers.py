import django_filters
from rest_framework import serializers

from main.models import Status, Tag, Task, User


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("username",)


class TaskFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    status = django_filters.CharFilter(lookup_expr="icontains")
    tags = django_filters.ModelMultipleChoiceFilter(
        name="tag__name",
        to_field_name="name",
        lookup_type="in",
        queryset=Tag.objects.all(),
    )
    author = django_filters.ModelChoiceFilter()

    class Meta:
        model = Task
        fields = (
            "title",
            "status",
            "tags",
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "phone",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = (
            "id",
            "name",
        )


class TaskSerializer(serializers.ModelSerializer):
    status = StatusSerializer()
    tags = TagSerializer()

    class Meta:
        model = Task
        fields = (
            "title",
            "description",
            "status",
            "priority",
            "start_at",
            "finish_until",
            "tags",
            "author",
            "assignee",
        )
