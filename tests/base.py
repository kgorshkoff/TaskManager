from http import HTTPStatus
from typing import List, Optional, Union

from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase

from main.models import User
from tests.factories.user_factory import UserFactory


class TestViewSetBase(APITestCase):
    user: User = None
    api_client: APIClient = None
    basename: str

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = cls.create_api_user()
        cls.api_client = APIClient()
        cls.api_client.force_authenticate(user=cls.user)

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
        self.api_client.force_authenticate(user=self.user)
        response = self.api_client.post(self.list_url(args), data=data)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.json()

    def list(self, data: dict = None, args: List[Union[str, int]] = None) -> List[dict]:
        response = self.api_client.get(self.list_url(args), data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    def retrieve(self, obj: dict, query_data: dict = None) -> dict:
        url = self.detail_url(obj["id"])
        response = self.api_client.get(url, query_data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    def update(self, obj: dict, attributes: dict, user: Optional[User] = None) -> dict:
        url = self.detail_url(obj["id"])
        response = self.api_client.put(url, data=attributes, user=user)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    def delete(self, obj: dict) -> None:
        url = self.detail_url(obj["id"])
        response = self.api_client.delete(url)
        assert response.status_code == HTTPStatus.NO_CONTENT

    def request_create(self, attributes: dict, args: List[Union[str, int]] = None):
        self.api_client.force_authenticate(user=self.user)
        return self.api_client.post(self.list_url(args), data=attributes)

    def request_single_resource(self, data: dict = None) -> Response:
        return self.api_client.get(self.list_url(), data=data)

    def single_resource(self, data: dict = None) -> dict:
        response = self.request_single_resource(data)
        assert response.status_code == HTTPStatus.OK
        return response.data

    def request_patch_single_resource(self, attributes: dict) -> Response:
        url = self.list_url()
        return self.api_client.patch(url, data=attributes)

    def patch_single_resource(self, attributes: dict) -> dict:
        response = self.request_patch_single_resource(attributes)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data
