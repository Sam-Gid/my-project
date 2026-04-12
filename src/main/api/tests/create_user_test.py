import pytest
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreateUser:
    def test_create_user_valid(self, api_manager):
        create_user_request = CreateUserRequest(username='Sam99', password='Pas!sw0rd', role='ROLE_USER')

        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role


    @pytest.mark.parametrize(
        'username, password',
        [
            ('Абг', 'Pas!sw0rd'),
            ('ab', 'Pas!sw0rd'),
            ('abv!', 'Pas!sw0rd'),
            ('Maxx1', 'Pas!sw0rд'),
            ('Maxx2', 'Pas!sw0'),
            ('Maxx3', 'pas!sw0rd'),
            ('Maxx4', 'PAS!SW0RD'),
            ('Maxx5', 'pasSsw0rd'),
            ('Maxx6', 'pasSsword'),
        ]
    )
    def test_create_user_invalid(self, username, password, api_manager):
        create_user_request = CreateUserRequest(username=username, password=password, role='ROLE_USER')

        api_manager.admin_steps.create_invalid_user(create_user_request)







