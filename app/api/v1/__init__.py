from fastapi import APIRouter

from app.api.v1.auth.routes import auth
from app.api.v1.post.routes import post
from app.api.v1.transaction.routes import transaction

main_router = APIRouter(prefix="/api/v1")

main_router.include_router(router=auth)
main_router.include_router(router=post)
main_router.include_router(router=transaction)