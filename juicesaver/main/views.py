from main import main_bp

@main_bp.route('/')
def index():
    return "index"
