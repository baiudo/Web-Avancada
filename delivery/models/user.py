from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func
from delivery.ext.db import db

if TYPE_CHECKING:
    from .role_user import RoleUser
    from .location import Address
    from .business import Business

# === User (usuario) ===
class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), index=True)
    email: Mapped[str] = mapped_column(db.String(100), unique=True, index=True)
    phone: Mapped[Optional[str]] = mapped_column(db.String(15))
    email_verified_at: Mapped[Optional[datetime]] = mapped_column(db.DateTime(timezone=True))
    photo: Mapped[Optional[str]] = mapped_column(db.String(100))
    password: Mapped[Optional[str]] = mapped_column(db.String(255))
    google_id: Mapped[Optional[str]] = mapped_column(db.String(255))
    facebook_id: Mapped[Optional[str]] = mapped_column(db.String(255))
    cpf: Mapped[Optional[str]] = mapped_column(db.String(15), index=True)

    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True), 
        server_default=func.now()
    )

    updated_at: Mapped[Optional[datetime]] = mapped_column(
        db.DateTime(timezone=True), 
        onupdate=func.now()
    )

    is_active: Mapped[bool] = mapped_column(
        db.Boolean,
        default=True,
        nullable=False,
        index=True
    )

    owned_businesses: Mapped[list["Business"]] = relationship(
        "Business",
        secondary="business_owners",
        back_populates="owners"
    )

    role_associations: Mapped[List["RoleUser"]] = relationship(
        "RoleUser",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    addresses: Mapped[List["Address"]] = relationship(
        "Address",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    @property
    def roles(self):
        return [assoc.role for assoc in self.role_associations if assoc.role]

    def __repr__(self) -> str:
        return f"<User {self.email}>"