from http import HTTPStatus

from django.core.files.uploadedfile import SimpleUploadedFile

from tests.base import TestViewSetBase
from tests.factories.user_factory import UserFactory


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes: dict

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user_attributes = UserFactory.build()

    @staticmethod
    def expected_details(entity: dict, attributes: dict) -> dict:
        del attributes["password"]
        return {**attributes, "id": entity["id"], "avatar_picture": entity["avatar_picture"]}

    def test_create(self) -> None:
        user = self.create(self.user_attributes)
        expected_response = self.expected_details(user, self.user_attributes)
        assert user == expected_response

    def test_filter(self):
        user1_attributes = UserFactory.build()
        user1 = self.create(data=user1_attributes)
        user2_attributes = UserFactory.build()
        user2 = self.create(data=user2_attributes)

        query = {"username": user1["username"]}
        response = self.list(query)
        assert [user1] == response

    def test_update(self) -> None:
        user = self.create(UserFactory.build())
        new_user_attributes = UserFactory.build()

        updated_user = self.update(user, new_user_attributes)

        expected_response = self.expected_details(updated_user, new_user_attributes)
        expected_response["avatar_picture"] = updated_user["avatar_picture"]

    def test_large_avatar(self) -> None:
        user_attributes = UserFactory.build(
            avatar_picture=SimpleUploadedFile("large.jpg", b"x" * 2 * 1024 * 1024)
        )
        response = self.request_create(user_attributes)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {"avatar_picture": ["Maximum size 1048576 exceeded."]}

    def test_avatar_bad_extension(self) -> None:
        user_attributes = UserFactory.build()
        user_attributes["avatar_picture"].name = "bad_extension.pdf"
        response = self.request_create(user_attributes)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {
            "avatar_picture": [
                "File extension “pdf” is not allowed. Allowed extensions are: jpeg, jpg, png."
            ]
        }