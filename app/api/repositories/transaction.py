from sqlalchemy.orm import Session
from app.core.base.repository import BaseRepository
from app.api.models.transaction import Transaction

class TransactionRepository(BaseRepository[Transaction]):
    """
    Transaction repository class for CRUD operations on Transaction model.
    This class provides a specific interface for performing CRUD operations on the Transaction model.
    It inherits from the BaseRepository class.
    Attributes:
        db (Session): The SQLAlchemy session.
    """

    def __init__(self, db: Session):
        """
        Initializes the TransactionRepository with a database session.
        Args:
            db (Session): The SQLAlchemy session to use for database operations.
        """
        super().__init__(Transaction, db)