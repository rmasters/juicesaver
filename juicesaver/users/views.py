from users import users_bp

@users_bp.route('/')
def list_users():
    return "list_users"


