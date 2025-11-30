from aiogram import Router

from .delete_lead import router as delete_lead_router


def setup_routers() -> Router:
    router = Router()
    router.include_router(delete_lead_router)
    return router
