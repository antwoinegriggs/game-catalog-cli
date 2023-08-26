from base import Base

from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

class Genre(Base):
    __tablename__ = "genres"
    __table_args__= (PrimaryKeyConstraint("id"),)

    id = Column(Integer(), primary_key=True)
    type = Column(String())

    def __repr__(self):
        return f"\n<Genre " \
            + f"id = {self.id}, " \
            + f"type = {self.type}" \
            +">"