from rest_framework.test import APIClient
import pytest


@pytest.mark.django_db
@pytest.mark.parametrize(
    "email, password, expected_result",
    [
        ("nikhithraj1@gmail.com", "1111111111", 200),
        ("nikhithraj2@gmail.com", "2222222222", 200),
        
    ]
)
def test_login(email, password, expected_result):
    client = APIClient()
    data = {
        "username":email,
        "password":password
    }
    response = client.post('/finder/login/login',data)
    assert response.status_code == expected_result
   