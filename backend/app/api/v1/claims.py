import hashlib
import uuid

from fastapi import APIRouter, status

from app.api.deps import CurrentUser, DatabaseSession
from app.models.career import CareerClaim, Evidence
from app.schemas.claims import CareerClaimCreate, CareerClaimRead, CareerClaimUpdate, EvidenceCreate, EvidenceRead
from app.services.claim_service import claim_service

router = APIRouter(prefix="/claims", tags=["Career Claims"])


@router.post("", response_model=CareerClaimRead, status_code=status.HTTP_201_CREATED)
def create_claim(payload: CareerClaimCreate, current_user: CurrentUser, db: DatabaseSession):
    claim = claim_service.create_claim(db, current_user, payload)
    return _serialize_claim(claim)


@router.get("", response_model=list[CareerClaimRead])
def list_claims(current_user: CurrentUser, db: DatabaseSession):
    return [_serialize_claim(claim) for claim in claim_service.list_claims(db, current_user)]


@router.get("/{claim_id}", response_model=CareerClaimRead)
def get_claim(claim_id: uuid.UUID, current_user: CurrentUser, db: DatabaseSession):
    return _serialize_claim(claim_service.get_claim(db, current_user, claim_id))


@router.put("/{claim_id}", response_model=CareerClaimRead)
def update_claim(claim_id: uuid.UUID, payload: CareerClaimUpdate, current_user: CurrentUser, db: DatabaseSession):
    return _serialize_claim(claim_service.update_claim(db, current_user, claim_id, payload))


@router.post("/{claim_id}/reject", response_model=CareerClaimRead)
def reject_claim(claim_id: uuid.UUID, current_user: CurrentUser, db: DatabaseSession):
    return _serialize_claim(claim_service.reject_claim(db, current_user, claim_id))


@router.post("/{claim_id}/evidence", response_model=EvidenceRead, status_code=status.HTTP_201_CREATED)
def add_evidence(claim_id: uuid.UUID, payload: EvidenceCreate, current_user: CurrentUser, db: DatabaseSession):
    evidence = claim_service.add_evidence(db, current_user, claim_id, payload)
    return _serialize_evidence(evidence)


@router.post("/{claim_id}/confirm", response_model=CareerClaimRead)
def confirm_claim(claim_id: uuid.UUID, current_user: CurrentUser, db: DatabaseSession):
    claim = claim_service.confirm_claim(db, current_user, claim_id)
    return _serialize_claim(claim)


def _serialize_claim(claim: CareerClaim) -> CareerClaimRead:
    return CareerClaimRead.model_validate(claim)


def _serialize_evidence(evidence: Evidence) -> EvidenceRead:
    return EvidenceRead.model_validate(evidence)
