from pydantic import BaseModel
from typing import List, Optional
from app.core.base.schema import BaseResponseModel


# Data model for Post
class PostData(BaseModel):
    id: str
    title: str
    content: str
    author_id: str
    created_at: str

# Request model for creating a new post
class CreatePostRequest(BaseModel):
    title: str
    content: str

# Request model for updating an existing post
class UpdatePostRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# Response model for a single post
class PostResponse(BaseResponseModel):
    data: PostData

# Response model for a list of posts
class PostListResponse(BaseResponseModel):
    data: List[PostData]