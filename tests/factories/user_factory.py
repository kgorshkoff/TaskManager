import factory
from factory import Faker, Factory

from tests.factories.base import ImageFileProvider

factory.Faker.add_provider(ImageFileProvider)


class UserFactory(Factory):
    username = Faker("user_name")
    password = Faker("password")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Faker("email")
    date_of_birth = Faker("date")
    phone = Faker("msisdn")
    avatar_picture = Faker("image_file", fmt="jpeg")

    class Meta:
        model = dict
