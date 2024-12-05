from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def login():
    return {'msg': 'Hello from router'}

@router.post('/')
async def register():
    pass