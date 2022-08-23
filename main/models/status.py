from django.db import models


class Status(models.TextChoices):
    NEW = "New task"
    IN_DEVELOPMENT = "In development"
    IN_QA = "In QA"
    IN_CODE_REVIEW = "In code review"
    READY_FOR_RELEASE = "Ready for release"
    RELEASED = "Released"
    ARCHIVED = "Archived"
