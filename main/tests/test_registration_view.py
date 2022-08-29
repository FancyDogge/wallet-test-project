import pytest


@pytest.mark.parametrize(
    "username, email, password, password2, validity",
    [
        ("user1", "asdfsf@gmail.com", "12345a", "12345a", 201), #full valid register data
        ("user1", "asdfsf@gmail.com", "12345a", "12345", 400), #passwords don't match
        ("user1", "", "12345a", "12345a", 201), #valid data, no email
        ("user1", "sdf23fff@ewd", "12345a", "12345a", 400), #valid data, except email
        ("user1", "asdfsf@gmail.com", "", "", 400), #No passwords
    ],
)
@pytest.mark.django_db
def test_create_account_view(client, username, email, password, password2, validity):
    response = client.post(
        "/register/",
        data={
            "username": username,
            "email": email,
            "password": password,
            "password2": password2,
        },
    )
    assert response.status_code == validity