from sqlmodel import Field, Session, SQLModel, create_engine, select, func, DateTime
from datetime import datetime
import sqlalchemy as sa


class Patron(SQLModel, table=True):
    __tablename__ = "Patrons"
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    phone: str
    weight: float
    gender: str
    birthdate: datetime
    created_at: datetime = Field(
        sa_column=sa.Column(sa.DateTime, server_default=sa.func.now())
    )
    updated_at: datetime = Field(
        sa_column=sa.Column(sa.DateTime, server_default=sa.func.now())
    )
    deleted_at: datetime | None = None

    def create_patron(self, session: Session):
        """Create a new patron"""
        session.add(self)
        session.commit()
        return self

    def __repr__(self):
        return f"Patron {self.name} with id {self.id}"

    def read_patrons(session: Session, page: int, per_page: int):
        """Retrieve a list of patrons"""
        query = select(Patron).limit(per_page).offset(page * per_page)
        patrons = session.exec(query)
        total = session.exec(select(func.count(Patron.id))).one()
        total_pages = total // per_page

        return patrons, total, total_pages

    def read_patron(session: Session, patron_id: int):
        """Retrieve a single patron"""
        patron = session.get(Patron, patron_id)
        return patron

    def update_patron(session: Session, patron_id: int, modified_patron: dict):
        """Update a patron"""
        patron = session.get(Patron, patron_id)
        modified_patron["updated_at"] = datetime.now()
        patron.sqlmodel_update(modified_patron)
        session.commit()
        return patron

    def delete_patron(session: Session, patron_id: int):
        """Delete a patron"""
        patron = session.get(Patron, patron_id)
        session.delete(patron)
        session.commit()
        return patron
