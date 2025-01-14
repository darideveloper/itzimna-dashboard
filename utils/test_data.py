from django.contrib.auth.models import User


def create_admin_user() -> tuple[str, str]:
    """ Create a new admin user and return it
    
    Returns:
        tuple:
            str: Username of the user created
            str: Password of the user created
            User: User created
    """
    
    # Create admin user
    password = "admin"
    user = User.objects.create_superuser(
        username="admin",
        email="test@gmail.com",
        password=password,
    )
    
    return user.username, password, user
