from fastapi import status, APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..db import services
from ..db.models import get_db
from ..utils import get_user_info
from datetime import datetime
from .schemas import GenerateProblemDTO
from ..generate_problem import generate_problem_by_coze
from json import loads, dumps
from ..constants import DEFAULT_QUOTA_REMAIN

router = APIRouter()


@router.get("/history")
async def get_history(request: Request, db: Session = Depends(get_db)):
    user_info = get_user_info(request)
    user_id = user_info.get("user_id")  # user_info["user_id"]
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    history = services.get_history(db, user_id)
    return {"history": history}


@router.get("/quota")
async def get_quota(request: Request, db: Session = Depends(get_db)):
    user_info = get_user_info(request)
    user_id = user_info.get("user_id")  # user_info["user_id"]
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    quota = services.get_quota(db, user_id)
    if quota is None:
        return {
            "user_id": user_id,
            "remain": DEFAULT_QUOTA_REMAIN,
            "last_reset_date": datetime.now(),
        }
    quota = services.reset_quota(db, user_id)
    return quota


@router.post("/generate/problem")
async def generate_problem(
    request: Request, dto: GenerateProblemDTO, db: Session = Depends(get_db)
):
    try:
        user_info = get_user_info(request)
        user_id = user_info.get("user_id")  # user_info["user_id"]
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )
        quota = services.get_quota(db, user_id)
        if quota is None:
            services.create_quota(db, user_id)
        quota = services.reset_quota(db, user_id)
        if quota.remain <= 0:  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="quota.remain <= 0",
            )

        problem = generate_problem_by_coze(level=dto.level)
        print("problem['options']:", problem["options"])

        new_problem = services.create_problem(
            db=db,
            created_by=user_id,
            level=dto.level,
            description=problem["description"],
            answer_id=int(problem["answer_id"]),
            solution=problem["solution"],
            options=dumps(problem["options"]),
            # **problem,
        )

        quota.remain -= 1  # type: ignore
        db.commit()
        return {
            "id": new_problem.id,
            "level": new_problem.level,
            "description": new_problem.description,
            "options": loads(new_problem.options),  # type: ignore
            "answer_id": new_problem.answer_id,
            "solution": new_problem.solution,
            "timestamp": new_problem.created_at.isoformat(),
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
