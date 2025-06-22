from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.models.post import Post
from app.api.models.user import User
from app.api.v1.post import schemas
from app.api.repositories.post import PostRepository
from app.utils.logger import logger

class PostService:
    """
    Post service class for handling post-related operations.
    This class provides methods for creating, updating, deleting, and retrieving posts.
    It interacts with the PostRepository to perform database operations.
    Attributes:
        db (Session): The SQLAlchemy session used for database operations.
    """

    def __init__(self, db: Session):
        """
        Initializes the PostService with a database session.

        Args:
            db (Session): The SQLAlchemy session to use for database operations.
        """
        self.repository = PostRepository(db)

    def create_post(self, post_data: schemas.CreatePostRequest, current_user: User) -> Post:
        """
        Creates a new post.

        Args:
            post_data (schemas.CreatePostRequest): The data for the new post.
            current_user (User): The user creating the post.

        Returns:
            Post: The created Post object.
        """

        try:
            post = Post(
                title=post_data.title,
                content=post_data.content,
                author_id=current_user.id
            )
            created_post = self.repository.create(post)
            logger.info(f"Post created successfully: {created_post.id}")
            return created_post
        except Exception as e:
            logger.error(f"Error creating post: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the post."
            )
        
    def update_post(self, post_id: str, post_data: schemas.UpdatePostRequest, current_user: User) -> Post:
        """
        Updates an existing post.

        Args:
            post_id (str): The ID of the post to update.
            post_data (schemas.UpdatePostRequest): The data to update the post with.
            current_user (User): The user updating the post.

        Returns:
            Post: The updated Post object.
        """
        
        post = self.repository.get_author_post_by_id(author_id=current_user.id, post_id=post_id)
        if not post:
            logger.warning(f"Post with ID {post_id} not found for author {current_user.id}.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found."
            )
        try:
            update_data = post_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(post, key, value)
            updated_post = self.repository.update(post)
            logger.info(f"Post updated successfully: {updated_post.id}")
            return updated_post
        except Exception as e:
            logger.error(f"Error updating post: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the post."
            )
        
    def delete_post(self, post_id: str, current_user: User) -> bool:
        """
        Deletes a post.

        Args:
            post_id (str): The ID of the post to delete.
            current_user (User): The user deleting the post.

        Returns:
            bool: True if the post was deleted successfully, False otherwise.
        """
        
        post = self.repository.get_author_post_by_id(author_id=current_user.id, post_id=post_id)
        if not post:
            logger.warning(f"Post with ID {post_id} not found for author {current_user.id}.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found."
            )
        try:
            self.repository.delete(post.id)
            logger.info(f"Post deleted successfully: {post.id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting post: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while deleting the post."
            )
        
    def get_post_by_id(self, post_id: str, current_user: User) -> Post:
        """
        Retrieves a post by its ID.

        Args:
            post_id (str): The ID of the post to retrieve.
            current_user (User): The user requesting the post.

        Returns:
            Post: The Post object if found, raises HTTPException if not found.
        """
        
        post = self.repository.get_author_post_by_id(author_id=current_user.id, post_id=post_id)
        if not post:
            logger.warning(f"Post with ID {post_id} not found for author {current_user.id}.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found."
            )
        return post
    
    def get_posts_by_author(self, author_id: str) -> List[Post]:
        """
        Retrieves all posts by a specific author.

        Args:
            author_id (str): The ID of the author whose posts are to be retrieved.

        Returns:
            List[Post]: A list of Post objects authored by the specified author.
        """
        
        try:
            posts = self.repository.get_posts_by_author(author_id=author_id)
            logger.info(f"Retrieved {len(posts)} posts for author {author_id}.")
            return posts
        except Exception as e:
            logger.error(f"Error retrieving posts for author {author_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while retrieving posts."
            )
        
    def get_all_posts(self) -> List[Post]:
        """
        Retrieves all posts.

        Returns:
            List[Post]: A list of all Post objects.
        """
        
        try:
            posts = self.repository.get_all()
            logger.info(f"Retrieved {len(posts)} posts from the database.")
            return posts
        except Exception as e:
            logger.error(f"Error retrieving all posts: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while retrieving posts."
            )