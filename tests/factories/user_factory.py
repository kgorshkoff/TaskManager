import factory


class UserFactory(factory.Factory):
    username = factory.Faker("user_name")
    password = factory.Faker("password")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    date_of_birth = factory.Faker("date")
    phone = factory.Faker("msisdn")

    class Meta:
        model = dict
