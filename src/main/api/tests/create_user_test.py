import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.user_crud import UserCrudDb as User


@pytest.mark.api
class TestCreateUser:
    def test_create_user_valid(self, api_manager: ApiManager, db_session: Session):
        create_user_request = RandomModelGenerator.generate(CreateUserRequest)
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username, 'Ошибка: Имя пользователя не соответствует запросу'
        assert create_user_request.role == response.role, 'Ошибка: Роль пользователя не соответствует запросу'

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username, 'Ошибка: Имя пользователя не найдено в БД'


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
    def test_create_user_invalid(self, username, password, api_manager, db_session: Session):
        create_user_request = CreateUserRequest(username=username, password=password, role='ROLE_USER')
        response = api_manager.admin_steps.create_invalid_user(create_user_request)
        assert response.status_code == 400

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db is None, 'Ошибка: Пользователь обнаружен в БД'