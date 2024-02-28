import datetime
from typing import List, Optional
from pydantic import BaseModel


class Post(BaseModel):
    title: str
    short_description: str
    description: str
    tags: List[str] = []
    created_at: Optional[datetime.datetime] = datetime.datetime.now()
    updated_at: Optional[datetime.datetime] = datetime.datetime.now()
