from http import HTTPStatus
from typing import List, Optional, Union

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import User
from tests.factories.user_factory import UserFactory


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    basename: str

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = cls.create_api_user()
        cls.client = APIClient()
        cls.client.force_authenticate(user=cls.user)

    @staticmethod
    def create_api_user() -> User:
        user_attributes = UserFactory.build()
        return User.objects.create_user(**user_attributes)

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url(args), data=data)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.json()

    def list(self, data: dict = None, args: List[Union[str, int]] = None) -> List[dict]:
        response = self.client.get(self.list_url(args), data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    def retrieve(self, obj: dict, query_data: dict = None) -> dict:
        url = self.detail_url(obj["id"])
        response = self.client.get(url, query_data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    def update(
        self, obj: dict, attributes: dict, user: Optional[User] = None
    ) -> dict:
        url = self.detail_url(obj["id"])
        response = self.client.put(url, data=attributes, user=user)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    def delete(self, obj: dict) -> None:
        url = self.detail_url(obj["id"])
        response = self.client.delete(url)
        assert response.status_code == HTTPStatus.NO_CONTENT

    def request_create(self, attributes: dict, args: List[Union[str, int]] = None):
        self.client.force_authenticate(user=self.user)
        return self.client.post(self.list_url(args), data=attributes)
