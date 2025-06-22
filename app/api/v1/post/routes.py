from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated

from app.db.database import get_db
from app.core.dependencies.security import get_current_user

from app.api.v1.post import schemas
from app.api.models.user import User
from app.api.services.post import PostService

post = APIRouter(prefix="/posts", tags=["Blog Posts"])


@post.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostResponse,
    summary="Create a new blog post",
    description="This endpoint allows users to create a new blog post.",
    tags=["Blog Posts"],
)
def create_post(
    post_data: schemas.CreatePostRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: User = Depends(get_current_user),
):
    """
    Endpoint to create a new blog post.

    Args:
        post_data (schemas.CreatePostRequest): The data for the new post.
        db (Annotated[Session, Depends]): The database session.
        current_user (User): The currently authenticated user.

    Returns:
        schemas.PostResponse: The created post data.
    """
    service = PostService(db=db)
    created_post = service.create_post(post_data=post_data, current_user=current_user)
    return schemas.PostResponse(
        status_code=status.HTTP_201_CREATED,
        message="Post created successfully",
        data=created_post.to_dict(),
    )

@post.get(
    path="/{post_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.PostResponse,
    summary="Get a blog post by ID",
    description="This endpoint allows users to retrieve a blog post by its ID.",
    tags=["Blog Posts"],
)
def get_post_by_id(
    post_id: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: User = Depends(get_current_user),
):
    """
    Endpoint to retrieve a blog post by its ID.

    Args:
        post_id (str): The ID of the post to retrieve.
        db (Annotated[Session, Depends]): The database session.
        current_user (User): The currently authenticated user.

    Returns:
        schemas.PostResponse: The retrieved post data.
    """
    service = PostService(db=db)
    post = service.get_post_by_id(post_id=post_id, current_user=current_user)
    
    return schemas.PostResponse(
        status_code=status.HTTP_200_OK,
        message="Post retrieved successfully",
        data=post.to_dict(),
    )

@post.get(
    path="/author/{author_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.PostListResponse,
    summary="Get all posts by author",
    description="This endpoint allows users to retrieve all blog posts by a specific author.",
    tags=["Blog Posts"],
)
def get_posts_by_author(
    author_id: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: User = Depends(get_current_user),
):
    """
    Endpoint to retrieve all blog posts by a specific author.

    Args:
        author_id (str): The ID of the author whose posts to retrieve.
        db (Annotated[Session, Depends]): The database session.
        current_user (User): The currently authenticated user.

    Returns:
        schemas.PostListResponse: The list of posts by the specified author.
    """
    service = PostService(db=db)
    posts = service.get_posts_by_author(author_id=author_id, current_user=current_user)
    
    return schemas.PostListResponse(
        status_code=status.HTTP_200_OK,
        message="Posts retrieved successfully",
        data=[post.to_dict() for post in posts],
    )

@post.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=schemas.PostListResponse,
    summary="Get all blog posts",
    description="This endpoint allows users to retrieve all blog posts.",
    tags=["Blog Posts"],
)
def get_all_posts(
    db: Annotated[Session, Depends(get_db)]
):
    """
    Endpoint to retrieve all blog posts.

    Args:
        db (Annotated[Session, Depends]): The database session.

    Returns:
        schemas.PostListResponse: The list of all blog posts.
    """
    service = PostService(db=db)
    posts = service.get_all_posts()
    
    return schemas.PostListResponse(
        status_code=status.HTTP_200_OK,
        message="All posts retrieved successfully",
        data=[post.to_dict() for post in posts],
    )

@post.delete(
    path="/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a blog post",
    description="This endpoint allows users to delete a blog post by its ID.",
    tags=["Blog Posts"],
)
def delete_post(
    post_id: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: User = Depends(get_current_user),
):
    """
    Endpoint to delete a blog post by its ID.

    Args:
        post_id (str): The ID of the post to delete.
        db (Annotated[Session, Depends]): The database session.
        current_user (User): The currently authenticated user.

    Returns:
        None: If the deletion is successful, returns no content.
    """
    service = PostService(db=db)
    service.delete_post(post_id=post_id, current_user=current_user)
    
    return {"message": "Post deleted successfully"}

@post.put(
    path="/{post_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.PostResponse,
    summary="Update a blog post",
    description="This endpoint allows users to update a blog post by its ID.",
    tags=["Blog Posts"],
)
def update_post(
    post_id: str,
    post_data: schemas.UpdatePostRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: User = Depends(get_current_user),
):
    """
    Endpoint to update a blog post by its ID.

    Args:
        post_id (str): The ID of the post to update.
        post_data (schemas.UpdatePostRequest): The data to update the post with.
        db (Annotated[Session, Depends]): The database session.
        current_user (User): The currently authenticated user.

    Returns:
        schemas.PostResponse: The updated post data.
    """
    service = PostService(db=db)
    updated_post = service.update_post(post_id=post_id, post_data=post_data, current_user=current_user)
    
    return schemas.PostResponse(
        status_code=status.HTTP_200_OK,
        message="Post updated successfully",
        data=updated_post.to_dict(),
    )