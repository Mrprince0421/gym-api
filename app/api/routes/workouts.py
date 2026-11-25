from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import User, Member, Workout, UserRole
from app.schemas.schemas import WorkoutCreate, WorkoutOut
from app.api.deps import get_current_user, require_roles
from app.core.cache import get_cache, set_cache, invalidate_cache_pattern

router = APIRouter(prefix="/workouts", tags=["Treinos"])

@router.post("", response_model=WorkoutOut, status_code=status.HTTP_201_CREATED)
def create_workout(
    payload: WorkoutCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.TRAINER)),
):
    member = db.query(Member).filter(Member.id == payload.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Membro não encontrado.")

    workout = Workout(
        member_id=payload.member_id,
        trainer_id=current_user.id,
        title=payload.title,
        description=payload.description,
    )
    db.add(workout)
    db.commit()
    db.refresh(workout)

    # Invalidação explícita do cache após mutação
    invalidate_cache_pattern("workouts:*")
    return workout

@router.get("", response_model=List[WorkoutOut])
def list_workouts(
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == UserRole.MEMBER:
        member = db.query(Member).filter(Member.user_id == current_user.id).first()
        if not member:
            return []
        cache_key = f"workouts:member:{member.id}"
        cached = get_cache(cache_key)
        if cached is not None:
            response.headers["X-Cache"] = "HIT"
            return cached

        workouts = db.query(Workout).filter(Workout.member_id == member.id).all()
        serialized = [WorkoutOut.model_validate(w).model_dump(mode="json") for w in workouts]
        set_cache(cache_key, serialized, ttl=60)
        response.headers["X-Cache"] = "MISS"
        return serialized

    cache_key = "workouts:all"
    cached = get_cache(cache_key)
    if cached is not None:
        response.headers["X-Cache"] = "HIT"
        return cached

    workouts = db.query(Workout).all()
    serialized = [WorkoutOut.model_validate(w).model_dump(mode="json") for w in workouts]
    set_cache(cache_key, serialized, ttl=60)
    response.headers["X-Cache"] = "MISS"
    return serialized