from sqlalchemy.orm import Session
from app.core.base.repository import BaseRepository
from app.api.models.post import Post

class PostRepository(BaseRepository[Post]):
    """
    Post repository class for CRUD operations on Post model.
    This class provides a specific interface for performing CRUD operations on the Post model.
    It inherits from the BaseRepository class.
    Attributes:
        db (Session): The SQLAlchemy session.
    """

    def __init__(self, db: Session):
        """
        Initializes the PostRepository with a database session.
        Args:
            db (Session): The SQLAlchemy session to use for database operations.
        """
        super().__init__(db, Post)

    def get_posts_by_author(self, author_id: str):
        """
        Retrieves all posts by a specific author.
        Args:
            author_id (str): The ID of the author whose posts are to be retrieved.
        Returns:
            List[Post]: A list of Post objects authored by the specified author.
        """
        return self.db.query(Post).filter(Post.author_id == author_id).all()
    
    def get_post_by_id(self, post_id: str):
        """
        Retrieves a post by its ID.
        Args:
            post_id (str): The ID of the post to retrieve.
        Returns:
            Post: The Post object with the specified ID, or None if not found.
        """
        return self.db.query(Post).filter(Post.id == post_id).first()
    
    def get_author_post_by_id(self, author_id: str, post_id: str):
        """
        Retrieves a post by its ID for a specific author.
        Args:
            author_id (str): The ID of the author.
            post_id (str): The ID of the post to retrieve.
        Returns:
            Post: The Post object if found, or None if not found or does not belong to the author.
        """
        return self.db.query(Post).filter(Post.author_id == author_id, Post.id == post_id).first()