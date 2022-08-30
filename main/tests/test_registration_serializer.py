import pytest
from main.serializers import RegistrationSerializer


# чтобы держать тестовые данные в одном месте и не плодить кучу тест кейсов
@pytest.mark.parametrize(
    "username, email, password, password2, validity",
    [
        ("user1", "sadjpij@gmail.com", "1234567ASd", "1234567ASd", True), #Valid Input Data
        ("user2", "fasdffs", "1234567ASd", "1234567ASd", False), #Invalid email
        (123125235, "sadjpij@gmail.com", "1234567ASd", "1234567ASd", False), #only nums username - как исправить? validate_name()?
        ("user3", "sadjpij@gmail.com", "", "", False), #Username and no passwords
        ("", "sadjpij@gmail.com", "1234567ASd", "1234567ASd", False), #No Username with passwords
        ("", "", "", "", False), #No Data
    ],
)
@pytest.mark.django_db
def test_account_registration(client, username, email, password, password2, validity):
    serializer = RegistrationSerializer(data={
        "username": username,
        "email": email,
        "password": password,
        "password2": password2,
    })
    print(serializer)
    assert serializer.is_valid() is validity