""" Post data model. """

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.base.model import BaseTableModel

class Post(BaseTableModel):
    """Post data model."""

    __tablename__ = "posts"

    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    author_id = Column(String, ForeignKey("users.id"), nullable=False)
    

    author = relationship("User", back_populates="posts")

    def __str__(self):
        return f"Post: {self.title} by {self.author.username}"
    
    def to_dict(self):
        """Convert Post instance to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author_id": self.author_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }