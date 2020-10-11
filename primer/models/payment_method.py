from datetime import datetime
import json
import uuid
from sqlalchemy import Column, String, ForeignKey
import sqlalchemy.dialects.postgresql as postgresql
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.exc import IntegrityError

from primer import db
from primer.exceptions import InvalidCustomer, InvalidPaymentProcessorPaymentInformation
from primer.tokenizer import Tokenizer

class PaymentMethod(db.Model):
    __tablename__ = 'payment_methods'
    id = Column(postgresql.UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4)
    customer_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('customers.id'), nullable=False)
    details = Column(MutableDict.as_mutable(postgresql.JSONB), nullable=False)
    token = Column(String(250), nullable=False)
    created_at = Column(postgresql.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(postgresql.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)

    @classmethod
    def create(kls, customer , details: dict):
        payment_method = PaymentMethod(
            customer_id = customer.id,
            details = details,
            token = Tokenizer.token_from(json.dumps(details))
        )

        try:
            db.session.add(payment_method)
            db.session.commit()
        except IntegrityError as err:
            error_info = err.orig.args[0]

            if 'customer_id' in error_info:
                raise InvalidCustomer
            else:
                raise err
        finally:
            db.session.rollback()

        return payment_method

    @classmethod
    def find_by_token(kls, token: str):
        return PaymentMethod.query.filter_by(
            token = token
        ).first()

    @classmethod
    def find_by_id(kls, id: uuid.UUID):
        return PaymentMethod.query.filter_by(
            id = id
        ).first()

    def as_dict(self):
        return {
            'token': self.token,
            'updated_at': int(self.created_at.timestamp()),
            'created_at': int(self.created_at.timestamp())
        }
