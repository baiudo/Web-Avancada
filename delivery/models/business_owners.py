from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from delivery.ext.db import db

if TYPE_CHECKING:
    from .user import User
    from .business import Business

# === BusinessOwner (Tabela Associativa N:N) ===
class BusinessOwner(db.Model):
    """
    Representa a copropriedade legal de um negocio.
    Esta classe resolve a relacao N:N entre Usuarios e Empresas.
    """
    __tablename__ = "business_owners"
    __table_args__ = {'extend_existing': True}

    # Chave primaria composta para garantir unicidade da relacao
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    business_id: Mapped[int] = mapped_column(ForeignKey("businesses.id"), primary_key=True)

    # Relacionamentos para navegacao direta via objeto de associacao
    user: Mapped["User"] = relationship(viewonly=True)
    business: Mapped["Business"] = relationship(viewonly=True)

    def __repr__(self) -> str:
        return f"<BusinessOwner user_id={self.user_id} business_id={self.business_id}>"