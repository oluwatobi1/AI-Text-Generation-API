import uuid
from app import db
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(32), primary_key=True, default=lambda: uuid.uuid4().hex ,unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)






    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"<User {self.username}>"
    

class GeneratedText(db.Model):
    id = db.Column(db.String(32), primary_key=True, default=lambda: uuid.uuid4().hex ,unique=True, nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey("users.id"), nullable=False)
    prompt = db.Column(db.Text, nullable=False)  
    response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default= db.func.current_timestamp())
