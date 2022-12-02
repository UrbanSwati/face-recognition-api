from pydantic import BaseModel

BUCKET_NAME='dima-face-recognition-project'

class Item(BaseModel):
    content: str