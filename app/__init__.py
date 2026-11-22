import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
from .config import config_map
from sqlalchemy import MetaData
from flask_bcrypt import Bcrypt

load_dotenv()


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app(config_name: str = None) -> Flask:
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "dev")

    app = Flask(__name__)
    app.config.from_object(config_map[config_name])
    # print(f"Running in config: {config_name}")

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "users.login"
    login_manager.login_message = "Будь ласка, увійдіть, щоб отримати доступ до цієї сторінки."
    login_manager.login_message_category = "warning"

    with app.app_context():
        from .views import main as main_blueprint
        app.register_blueprint(main_blueprint)

        from .users import users_bp
        from .users import models as user_models
        app.register_blueprint(users_bp)

        from .products import products_bp
        from .products import models as product_models
        app.register_blueprint(products_bp)

        from .posts import post_bp
        from .posts import models
        app.register_blueprint(post_bp)

        @app.errorhandler(404)
        def not_found(e):
            return render_template("404.html"), 404

        # if config_name == "test":
        #     print("Registered routes:")
        #     for rule in app.url_map.iter_rules():
        #         print(rule)

    return app