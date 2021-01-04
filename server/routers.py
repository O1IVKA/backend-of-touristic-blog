from app.city import city
from app.country import country
from app.news.endpoints import post, comment, like, tags
from app.users.endpoints import user
from fastapi import APIRouter

router = APIRouter()

router.include_router(user.router, prefix="/user", tags=["user"])

router.include_router(post.router, prefix="/post", tags=["Articles"])
router.include_router(tags.router, prefix="/tag", tags=["Tags"])
router.include_router(comment.router, prefix="/comment", tags=["Comments"])
router.include_router(like.router, prefix="/like", tags=["Likes"])

router.include_router(country.router, prefix="/country", tags=["Countries"])
router.include_router(city.router, prefix="/city", tags=["Cities"])



