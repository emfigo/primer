from datetime import datetime
import uuid
from sqlalchemy import Column, String
import sqlalchemy.dialects.postgresql as postgresql

from primer import db
from primer.tokenizer import Tokenizer

class Customer(db.Model):
    __tablename__ = 'customers'
    id = Column(postgresql.UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    company = Column(String(50))
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(100), nullable=False)
    fax = Column(String(20))
    website = Column(String(250))
    token = Column(String(250), nullable=False)
    created_at = Column(postgresql.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(postgresql.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)

    @classmethod
    def create(kls,
               first_name: str,
               last_name: str,
               company: str,
               email: str,
               phone: str = None,
               fax: str = None,
               website: str = None):

        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            company=company,
            email=email,
            phone=phone,
            fax=fax,
            website=website,
            token=Tokenizer.random_token()
        )

        db.session.add(customer)
        db.session.commit()

        return customer

    @classmethod
    def find_by_email(kls, email: str):
        return kls.query.filter_by(
            email = email
        ).first()

    @classmethod
    def find_by_id(kls, id: uuid.UUID):
        return kls.query.filter_by(
            id = id
        ).first()

    @classmethod
    def find_by_token(kls, token: str):
        return kls.query.filter_by(
            token = token
        ).first()
