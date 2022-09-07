from tests.base import TestViewSetBase
from tests.factories.user_factory import UserFactory


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = UserFactory.build()

    @staticmethod
    def expected_details(entity: dict, attributes: dict) -> dict:
        del attributes["password"]
        return {**attributes, "id": entity["id"]}

    def test_create(self) -> None:
        user = self.create(self.user_attributes)
        expected_response = self.expected_details(user, self.user_attributes)
        assert user == expected_response

    def test_filter(self):
        user1 = self.create(data=self.user_attributes)
        user2_attributes = UserFactory.build(is_excess=True)
        user2 = self.create(data=user2_attributes)

        query = {"username": user1["username"]}
        response = self.list(query)
        assert [user1] == response
