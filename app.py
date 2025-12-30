from flask import Flask
from flask_login import LoginManager
from routes.auth import auth
from routes.vm import vm
from routes.admin import admin
from utils.database import get_user_by_id
from models.user import User

app = Flask(__name__)
app.secret_key = "supersegreto"

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    row = get_user_by_id(user_id)
    if row:
        return User(row[0], row[1], row[2], row[3])
    return None

app.register_blueprint(auth)
app.register_blueprint(vm)
app.register_blueprint(admin)

if __name__ == "__main__":
    app.run(debug=True)