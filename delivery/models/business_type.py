from typing import List, Optional, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from delivery.ext.db import db

if TYPE_CHECKING:
    from .business import Business

class BusinessType(db.Model):
    __tablename__ = "business_types"
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(80), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(db.String(255))
    status: Mapped[bool] = mapped_column(db.Boolean, default=True, nullable=False)
    
    businesses: Mapped[List["Business"]] = relationship(
        "Business",
        back_populates="business_type"
    )
    
    def __repr__(self) -> str:
        return f"<BusinessType {self.name}>"