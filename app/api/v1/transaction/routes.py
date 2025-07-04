from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated

from app.db.database import get_db

from app.api.v1.transaction import schemas
from app.api.services.transaction import TransactionService

transaction = APIRouter(prefix="/transaction", tags=["Transactions"])

@transaction.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.CreateTransactionResponse,
    summary="Create a new transaction",
    description="This endpoint allows users to create a new transaction.",
    tags=["Transactions"],
)
def create_transaction(
    transaction_data: schemas.CreateTransactionRequest,
    db: Annotated[Session, Depends(get_db)],
):
    """
    Endpoint to create a new transaction.

    Args:
        transaction_data (schemas.CreateTransactionRequest): The data for the new transaction.
        db (Annotated[Session, Depends]): The database session.
        current_user (str): The currently authenticated user.

    Returns:
        schemas.CreateTransactionResponse: The created transaction data.
    """
    service = TransactionService(db=db)
    created_transaction = service.create_transaction(transaction_data=transaction_data)
    return schemas.CreateTransactionResponse(
        status_code=status.HTTP_201_CREATED,
        message="Transaction created successfully",
        data=created_transaction.to_dict(),
    )

@transaction.get(
    path="/{transaction_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.TransactionResponse,
    summary="Get a transaction by ID",
    description="This endpoint allows users to retrieve a transaction by its ID.",
    tags=["Transactions"],
)
def get_transaction_by_id(
    transaction_id: str,
    db: Annotated[Session, Depends(get_db)],
):
    """
    Endpoint to retrieve a transaction by its ID.

    Args:
        transaction_id (str): The ID of the transaction to retrieve.
        db (Annotated[Session, Depends]): The database session.
        current_user (str): The currently authenticated user.

    Returns:
        schemas.TransactionResponse: The retrieved transaction data.
    """
    service = TransactionService(db=db)
    transaction = service.get_transaction(id=transaction_id)
    return schemas.TransactionResponse(
        status_code=status.HTTP_200_OK,
        message="Transaction retrieved successfully",
        data=transaction.to_dict(),
    )