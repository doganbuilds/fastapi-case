import datetime
from typing import List, Annotated
from app.model import Post

from google.cloud import firestore
from google.cloud.firestore import FieldFilter

from fastapi import HTTPException, Path, status


class PostService:
    def __init__(self, client: firestore.Client):
        try:
            self.client = client
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def get_all(self) -> List[Post]:
        posts = self.client.collection("posts").get()
        return [post.to_dict() for post in posts]

    def get_one(
        self,
        post_title: Annotated[str, Path(title="Title of the post you want to fetch")],
    ) -> Post:
        post = self.client.collection("posts").where("title", "==", post_title).get()
        return post[0].to_dict() if post else {}

    def create(
        self, post: Annotated[Post, Path(title="Post data from model.py")]
    ) -> Post:
        # check doc, validate post
        post.created_at = datetime.datetime.now()
        post.updated_at = datetime.datetime.now()
        doc = self.client.collection("posts").add(post.model_dump())
        return post

    def update(
        self,
        title: Annotated[str, Path(title="Title of the post you want to update")],
        post: Annotated[Post, Path(title="Post data from model.py")],
    ) -> Post:
        post_record = self.client.collection("posts").where("title", "==", title).get()
        post_ref = self.client.collection("posts").document(post_record[0].id)
        post.updated_at = datetime.datetime.now()
        post_ref.update(post.model_dump())
        return post

    def delete(
        self, title: Annotated[str, Path(title="Title of the post you want to delete")]
    ) -> dict[str, str]:
        post_record = self.client.collection("posts").where("title", "==", title).get()
        post_ref = self.client.collection("posts").document(post_record[0].id)
        post_ref.delete()
        return {"message": f"Post with title '{title}' deleted successfully"}

    def search(
        self,
        title: Annotated[
            str | None, Path(title="Search term to search for posts by title")
        ] = None,
        tag: Annotated[
            str | None, Path(title="Search term to search for posts by tags")
        ] = None,
    ):
        if title:
            posts = (
                self.client.collection("posts")
                .order_by("title")
                .start_at([title])
                .end_at([title + "\uf8ff"])
                .get()
            )
            return [post.to_dict() for post in posts]
        elif tag:
            posts = (
                self.client.collection("posts")
                .where(filter=FieldFilter("tags", "array_contains", tag))
                .get()
            )
            return [post.to_dict() for post in posts]
        else:
            return []
