from config import app
from controller import index, register, success, logout, login, dashboard, make_wish, create_wish, edit_page, edit_wish, grant_wish, like_wish, view_stats

# LOGIN ROUTES
app.add_url_rule('/', view_func= index)
app.add_url_rule('/register', view_func= register, methods=["POST"])
app.add_url_rule('/logout', view_func= logout)
app.add_url_rule('/success', view_func= login, methods=["POST"])
app.add_url_rule('/dashboard', view_func= dashboard)

# WISH ROUTES
app.add_url_rule('/make_wish', view_func= make_wish)
app.add_url_rule('/create_wish', view_func= create_wish, methods=["POST"])
app.add_url_rule('/edit_wish/<id>', view_func= edit_page)
app.add_url_rule('/update_wish/<id>', view_func= edit_wish, methods=["POST"])
app.add_url_rule('/grant_wish/<id>', view_func= grant_wish)
app.add_url_rule('/like_wish/<id>', view_func= like_wish)
app.add_url_rule('/view_stats', view_func= view_stats)