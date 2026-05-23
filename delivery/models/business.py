from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, ForeignKey, Integer, String, Boolean, DateTime
from delivery.ext.db import db

if TYPE_CHECKING:
    from .user import User
    from .role_user import RoleUser
    from .business_type import BusinessType
    from .business_owners import BusinessOwner
    from .location import Address


# === Business (empresa / estabelecimento) ===
class Business(db.Model):
    __tablename__ = "businesses"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    corporate_name: Mapped[str] = mapped_column(String(120), nullable=False)
    trade_name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    cnpj: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    business_type_id: Mapped[int] = mapped_column(ForeignKey("business_types.id"), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    # RELACAO N:N REAL
    # Agora uma empresa pode ter uma lista de owners
    owners: Mapped[list["User"]] = relationship(
        "User",
        secondary="business_owners",
        back_populates="owned_businesses"
    )

    # Relacionamento com Endereço (1:1)
    # Cascade garante que se a empresa sumir, o endereço dela também some.
    address: Mapped[Optional["Address"]] = relationship(
        "Address",
        back_populates="business",
        cascade="all, delete-orphan",
        uselist=False
    )

    role_associations: Mapped[List["RoleUser"]] = relationship(
        "RoleUser",
        back_populates="business",
        cascade="all, delete-orphan"
    )

    business_type: Mapped["BusinessType"] = relationship(
        "BusinessType",
        back_populates="businesses"
    )

    def __repr__(self) -> str:
        return f"<Business {self.trade_name}>"