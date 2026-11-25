from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import User, Member, CheckIn, UserRole
from app.schemas.schemas import CheckInCreate, CheckInOut
from app.api.deps import get_current_user

router = APIRouter(prefix="/checkins", tags=["Check-ins"])

@router.post("", response_model=CheckInOut, status_code=status.HTTP_201_CREATED)
def register_checkin(
    payload: CheckInCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    member = db.query(Member).filter(Member.id == payload.member_id).first()
    if not member or not member.active:
        raise HTTPException(status_code=404, detail="Membro não encontrado ou inativo.")

    if current_user.role == UserRole.MEMBER and member.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você só pode registrar check-in para si mesmo.")

    checkin = CheckIn(member_id=member.id)
    db.add(checkin)
    db.commit()
    db.refresh(checkin)
    return checkin

@router.get("", response_model=List[CheckInOut])
def list_checkins(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == UserRole.MEMBER:
        member = db.query(Member).filter(Member.user_id == current_user.id).first()
        if not member:
            return []
        return db.query(CheckIn).filter(CheckIn.member_id == member.id).all()

    return db.query(CheckIn).all()