from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserLogin

class UserService:
    @staticmethod
    def get_users(db: Session):
        return db.query(User).all()

    @staticmethod
    def get_user(user_id: int, db: Session):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create_user(user: UserCreate, db: Session):
        db_user = User(name=user.name, fullname=user.fullname, password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def login_user(user: UserLogin, db: Session):
        return db.query(User).filter(User.name == user.name).first()