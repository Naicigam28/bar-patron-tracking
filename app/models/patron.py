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

    def read_patrons(session: Session, page: int, per_page: int,paganate: bool = True):
        """Retrieve a list of patrons"""
        query = select(Patron).limit(per_page).offset(page * per_page)
        if paganate:
            query = select(Patron)
        patrons = session.exec(query)
        total = session.exec(select(func.count(Patron.id))).one()
        total_pages = total // per_page
        if paganate:
            return patrons, total, total_pages
        return patrons

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


class PatronDrink(SQLModel, table=True):
    """Track Patron Drinks"""

    __tablename__ = "PatronDrinks"
    id: int | None = Field(default=None, primary_key=True)
    patron_id: int
    drink_id: int
    created_at: datetime = Field(
        sa_column=sa.Column(sa.DateTime, server_default=sa.func.now())
    )
    updated_at: datetime = Field(
        sa_column=sa.Column(
            sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()
        )
    )
    deleted_at: datetime | None = None
    alcohol_type: str
    volume: float
    abv: float

    def create_patron_drink(self, session: Session):
        """Create a new patron drink"""
        session.add(self)
        session.commit()
        return self

    def list_patron_drinks(session: Session, patron_id: int, page: int, per_page: int):
        """List all drinks for a patron. Results are paganated and ordered by creation date"""
        query = (
            select(PatronDrink)
            .where(PatronDrink.patron_id == patron_id)
            .limit(per_page)
            .offset(page * per_page)
            .order_by(PatronDrink.created_at)
        )
        patron_drinks = session.exec(query).all()
        total = session.exec(
            select(func.count(PatronDrink.id)).where(PatronDrink.patron_id == patron_id)
        ).one()

        total_pages = total // per_page


        return patron_drinks, total, total_pages

    def __repr__(self):
        return f"PatronDrink {self.id} with patron_id {self.patron_id} and drink_id {self.drink_id}"
