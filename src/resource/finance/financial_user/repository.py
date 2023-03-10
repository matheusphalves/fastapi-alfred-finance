from sqlalchemy.orm import Session

from src.database.models import FinancialUser
from src.util.base_repository import BaseRepository


class FinancialUserRepository(BaseRepository):

    def __init__(self):
        self.entityModel = FinancialUser

    def update(self, db: Session, financial_user: FinancialUser) -> any:
        if self.exists_by_id(db, financial_user.id):
            return super().update(db, financial_user)
        return None

    def get_user_by_login(self, db:Session, login: str) -> any:
        return self.find_by_custom_column_value(db, "login", login).first()