from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import User, Member, UserRole
from app.schemas.schemas import MemberCreate, MemberOut
from app.core.security import get_password_hash
from app.api.deps import get_current_user, require_roles

router = APIRouter(prefix="/members", tags=["Membros"])

@router.post("", response_model=MemberOut, status_code=status.HTTP_201_CREATED)
def create_member(
    payload: MemberCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMIN)),
):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

    user = User(
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
        role=UserRole.MEMBER,
    )
    db.add(user)
    db.flush()

    member = Member(
        user_id=user.id,
        full_name=payload.full_name,
        phone=payload.phone,
        plan_name=payload.plan_name,
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

@router.get("", response_model=List[MemberOut])
def list_members(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.ADMIN, UserRole.TRAINER)),
):
    return db.query(Member).all()

@router.get("/{member_id}", response_model=MemberOut)
def get_member(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Membro não encontrado.")

    # Autorização a nível de objeto: member só consulta o próprio perfil
    if current_user.role == UserRole.MEMBER and member.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acesso negado a este perfil.")

    return member