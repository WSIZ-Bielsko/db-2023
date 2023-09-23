import datetime
from enum import IntEnum
from uuid import UUID

from pydantic import BaseModel
from src.praktyki.model import Role


class Document(BaseModel):
    """
    Data representing an immutable copy of dataclasses representing filled
    "documents" present in the system, to be signed by actors.

    "All entities looking like a sheet of paper (potentially signable)"

    Documents are immutable i.e. once created they are saved and can only be signed.
    If changes are needed, new versions must be created and signed again.

    """

    id: UUID  # same as id of all objects cast to Document (e.g. Application.id, InternshipAgreement.id)

    created_at: datetime.datetime
    json_repr: bytes | None  # json of the object
    sha256: str  # sha256 of `data` (if present), or `json`

    # FILES
    filename: str | None  # for files
    data: bytes | None  # for files

    class Config:
        allow_mutation = False


class SignatureText(BaseModel):
    # can generate pdf from this object (present on page)
    id: UUID
    document_id: UUID
    person_id: UUID
    document_sha256: str
    verbal: str  # should contain document_id, document_sha256, person_id

    class Config:
        allow_mutation = False


class SignatureType(IntEnum):
    CLICK = 0
    CLICK_OTP = 1
    HAND_WRITTEN = 2
    QESIG = 3
    WSIZ_ECDSA_PKEY_NSIT384p = 4  # like CLICK_OTP, but with SHA256 of the Document signed by a key


class Signature(BaseModel):
    """
    This class represents signatures + metadata associated with them (who signed, what roles did he have,
    what the id of the document was, etc.).

    Note:
        - the actual signature is in the .data field. It can be used for verification of QESig, or
        it can contain the pdf/png file of a scanned signed document,
        - what is actually signed is the SignatureText.document_sha256, which is the hash of the
        json (or pdf) of a Signable object.

    """
    id: UUID
    document_id: UUID
    signature_text_id: UUID  # signature text which is the verbal representation of what is signed
    person_id: UUID
    person_roles_at_signing: list[Role]  # roles the signatory had at the time of signing

    signed_at: datetime.date
    type: SignatureType
    data: bytes  # scanned file, or QESig signature
    keyid: UUID | None  # for WSIZ_PKEY, if such signature is used


class ECDSA_Key(BaseModel):
    key_id: UUID
    key: bytes
    pub: bytes
    owner_person_id: UUID
    created_at: datetime.datetime
    invalid_after: datetime.datetime
