from app.models import User, db

class UserRepository:
    @staticmethod
    def get_user_by_username( username):
        return User.query.filter_by(username=username).first()
    @staticmethod
    def create_user(username, password):
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
   
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)