from fastapi import APIRouter, Request, HTTPException, Depends
from ..db import services
from ..db.models import get_db
from svix.webhooks import Webhook
from sqlalchemy.orm import Session
from os import getenv
from json import loads

router = APIRouter()

clerk_webhook_secret = getenv("CLERK_WEBHOOK_SECRET")


@router.post("/user-created")
async def handler_user_created(request: Request, db: Session = Depends(get_db)):
    if clerk_webhook_secret is None:
        raise HTTPException(status_code=500, detail="CLERK_WEBHOOK_SECRET is None")

    body = await request.body()
    payload_str = body.decode("utf-8")
    headers = dict(request.headers)

    try:
        webhook = Webhook(clerk_webhook_secret)
        webhook.verify(payload_str, headers)
        payload = loads(payload_str)
        if payload.get("type") != "user.created":
            return {"status": "passed"}
        user_data = payload.get("data", {})
        user_id = user_data.get("id")
        if user_id is None:
            raise HTTPException(status_code=400, detail="user_id is None")
        services.create_quota(db, user_id)
        return {"status": "ok"}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
