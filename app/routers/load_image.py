from fastapi import APIRouter, status
from app.util import Item

router = APIRouter()


@router.post("/load", status_code=status.HTTP_200_OK)
async def add_image(item: Item):
    
    return {"Image": "Created"}