from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.models.transaction import Transaction
from app.api.repositories.transaction import TransactionRepository
from app.api.v1.transaction.schemas import CreateTransactionRequest
from app.utils.logger import logger


class TransactionService:
    """
    Transaction service class for handling transaction-related operations.
    This class provides methods for creating, updating, deleting, and retrieving transactions.
    It interacts with the TransactionRepository to perform database operations.
    Attributes:
        db (Session): The SQLAlchemy session used for database operations.
    """

    def __init__(self, db: Session):
        """
        Initializes the TransactionService with a database session.

        Args:
            db (Session): The SQLAlchemy session to use for database operations.
        """
        self.repository = TransactionRepository(db)

    def create_transaction(self, transaction_data: CreateTransactionRequest) -> Transaction:
        """
        Creates a new transaction.

        Args:
            transaction_data (CreateTransactionRequest): The data for the new transaction.

        Returns:
            Transaction: The created Transaction object.
        """
        try:
            transaction = Transaction(
                email=transaction_data.email,
                amount=transaction_data.amount,
                type=transaction_data.type
            )
            created_transaction = self.repository.create(transaction)
            logger.info(f"Transaction created successfully: {created_transaction.id}")
            return created_transaction
        except Exception as e:
            logger.error(f"Error creating transaction: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the transaction."
            )
        
    def get_transaction(self, id: str) -> Transaction:
        """
        Retrieves a transaction by its ID.

        Args:
            transaction_id (str): The ID of the transaction to retrieve.

        Returns:
            Transaction: The retrieved Transaction object.

        Raises:
            HTTPException: If the transaction is not found.
        """
        transaction = self.repository.get(id)
        if not transaction:
            logger.warning(f"Transaction with id {id} not found.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found."
            )
        return transaction
