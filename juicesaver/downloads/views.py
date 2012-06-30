from downloads import downloads_bp

@downloads_bp.route('/')
def list_downloads():
    return "list_downloads"

