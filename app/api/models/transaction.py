""" Transaction data model """

# Transaction table
    # email (string)
    # amount (float)
    # type (string)

from sqlalchemy import Column, String, Float
from app.core.base.model import BaseTableModel

class Transaction(BaseTableModel):

    __tablename__ = "transactions"

    email = Column(String, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)

    def __str__(self):
        return f"Transaction(id={self.id}, email={self.email}, amount={self.amount}, type={self.type})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "amount": self.amount,
            "type": self.type,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }