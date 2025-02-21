from sqlmodel import Field, Session, SQLModel, create_engine, select, func, DateTime
from datetime import datetime


class Patron(SQLModel, table=True):
    __tablename__ = "Patrons"
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    phone: str
    weight: float
    gender: str
    birthdate: DateTime
    created_at: DateTime = Field(default=datetime.now)
    updated_at: DateTime = Field(default=datetime.now)
    deleted_at: DateTime | None = None

    def __repr__(self):
        return f"Patron {self.name} with id {self.id}"

    def read_patrons(session: Session, page: int, per_page: int):
        """Retrieve a list of patrons"""
        query = select(Patron).limit(per_page).offset(page * per_page)
        patrons = session.exec(query)
        total = session.exec(select(func.count(Patron.id))).one()
        total_pages = total // per_page

        return patrons, total, total_pages

    def read_patron(self, session: Session, patron_id: int):
        """Retrieve a single patron"""
        patron = session.get(Patron, patron_id)
        return patron

    def create_patron(self, session: Session):
        """Create a new patron"""
        session.add(self)
        session.commit()
        return self

    def update_patron(self, session: Session, patron_id: int):
        """Update a patron"""
        patron = session.get(Patron, patron_id)
        session.update(patron)
        session.commit()
        return patron

    def delete_patron(self, session: Session, patron_id: int):
        """Delete a patron"""
        patron = session.get(Patron, patron_id)
        session.delete(patron)
        session.commit()
        return patron
