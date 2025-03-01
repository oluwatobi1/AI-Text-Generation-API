from app import create_app, db
from app.config import Config
from flask_migrate import Migrate

app = create_app()
migration = Migrate(app, db)

with app.app_context():
    db.create_all() 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT, debug=True)
