import pytest
from ava_prime_integration import Role, Permission, ROLE_PERMISSIONS, User, UserManager, require_permission

# Test User class
class TestUser:
    @pytest.fixture
    def admin_user(self):
        return User("user_001", "admin@codessa.ai", [Role.ADMIN])

    @pytest.fixture
    def developer_user(self):
        return User("user_002", "dev@codessa.ai", [Role.DEVELOPER])

    @pytest.fixture
    def viewer_user(self):
        return User("user_003", "viewer@codessa.ai", [Role.VIEWER])

    def test_has_permission_admin(self, admin_user):
        for permission in Permission:
            assert admin_user.has_permission(permission), f"Admin should have {permission}"

    def test_has_permission_developer(self, developer_user):
        assert developer_user.has_permission(Permission.RUN_AI_PROMPTS)
        assert developer_user.has_permission(Permission.VIEW_DASHBOARDS)
        assert not developer_user.has_permission(Permission.EXECUTE_COMMANDS)

    def test_has_permission_viewer(self, viewer_user):
        assert viewer_user.has_permission(Permission.VIEW_DASHBOARDS)
        assert not viewer_user.has_permission(Permission.RUN_AI_PROMPTS)
        assert not viewer_user.has_permission(Permission.EXECUTE_COMMANDS)

    def test_has_role(self, admin_user):
        assert admin_user.has_role(Role.ADMIN)
        assert not admin_user.has_role(Role.DEVELOPER)

    def test_update_last_login(self, admin_user):
        import time
        old_time = admin_user.last_login
        admin_user.update_last_login()
        assert admin_user.last_login is not None
        assert admin_user.last_login > (old_time or time.time() - 1)  # Approximate check

# Test UserManager class
class TestUserManager:
    @pytest.fixture
    def manager(self):
        return UserManager()

    def test_load_default_users(self, manager):
        assert len(manager.users) == 3
        assert "user_001" in manager.users
        assert manager.users["user_001"].email == "admin@codessa.ai"

    def test_get_user(self, manager):
        user = manager.get_user("user_001")
        assert user is not None
        assert user.email == "admin@codessa.ai"
        assert manager.get_user("invalid") is None

    def test_authenticate_user(self, manager):
        user = manager.authenticate_user("admin@codessa.ai")
        assert user is not None
        assert user.last_login is not None
        assert manager.authenticate_user("invalid@email.com") is None

# Test require_permission decorator
class TestRequirePermission:
    @pytest.fixture
    def admin_user(self):
        return User("user_001", "admin@codessa.ai", [Role.ADMIN])

    @pytest.fixture
    def viewer_user(self):
        return User("user_003", "viewer@codessa.ai", [Role.VIEWER])

    def test_require_permission_success(self, admin_user):
        @require_permission(Permission.EXECUTE_COMMANDS)
        def protected_func(user):
            return "Success"

        result = protected_func(admin_user)
        assert result == "Success"

    def test_require_permission_failure(self, viewer_user):
        @require_permission(Permission.EXECUTE_COMMANDS)
        def protected_func(user):
            return "Success"

        with pytest.raises(PermissionError):
            protected_func(viewer_user)