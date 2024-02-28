from fastapi import APIRouter, status

from typing import List

from firebase_admin import credentials, firestore
import firebase_admin

from app.model import Post
from app.service import PostService
from app.config import Settings

settings = Settings()

cred = credentials.Certificate(settings.firebase_certificate)
firebase_admin.initialize_app(cred)
client = firestore.client()

router = APIRouter()
service = PostService(client)


# Create new post
@router.post(
    "/",
    response_model=Post,
    status_code=status.HTTP_201_CREATED,
    tags=["posts"],
    summary="Creates new `Post`",
)
def create_post(post: Post) -> Post:
    return service.create(post)


# Get all posts
@router.get(
    "/",
    response_model=List[Post],
    status_code=status.HTTP_200_OK,
    tags=["posts", "get_all_posts"],
    summary="Get all posts",
)
def get_posts() -> List[Post]:
    return service.get_all()


# Get single post with title
@router.get(
    "/{title}",
    response_model=Post,
    status_code=status.HTTP_200_OK,
    tags=["posts", "get_single_post"],
    summary="Get single post",
)
def get_post(title: str) -> Post:
    return service.get_one(title)


# Update post with title
@router.put(
    "/{title}",
    response_model=Post,
    status_code=status.HTTP_200_OK,
    tags=["posts", "update_post"],
    summary="Update post",
)
def update_post(title: str, post: Post) -> Post:
    return service.update(title, post)


# Delete post with title
@router.delete(
    "/{title}",
    status_code=status.HTTP_200_OK,
    tags=["posts", "delete_post"],
    summary="Delete post",
)
def delete_post(title: str) -> dict[str, str]:
    return service.delete(title)


@router.get(
    "/search",
    response_model=List[Post],
    status_code=status.HTTP_200_OK,
    tags=["posts", "search"],
    summary="Search posts",
)
def search(title: str | None = None, tag: str | None = None) -> List[Post]:
    return service.search(title, tag)
