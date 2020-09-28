from datetime import datetime
import json
import uuid
from sqlalchemy import Column, String, ForeignKey
import sqlalchemy.dialects.postgresql as postgresql
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.exc import IntegrityError

from primer import db
from primer.exceptions import InvalidCustomer, InvalidPaymentProcessorInformation
from primer.tokenizer import Tokenizer

class PaymentMethod(db.Model):
    __tablename__ = 'payment_methods'
    id = Column(postgresql.UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4)
    customer_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('customers.id'), nullable=False)
    details = Column(MutableDict.as_mutable(postgresql.JSONB), nullable=False)
    payment_processor_information_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('payment_processor_informations.id'), nullable=False)
    token = Column(String(250), nullable=False)
    created_at = Column(postgresql.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(postgresql.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)

    @classmethod
    def create(kls, customer , details: dict, payment_processor_information):
        payment_method = PaymentMethod(
            customer_id = customer.id,
            details = details,
            payment_processor_information_id = payment_processor_information.id,
            token = Tokenizer.token_from(json.dumps(details))
        )

        try:
            db.session.add(payment_method)
            db.session.commit()
        except IntegrityError as err:
            error_info = err.orig.args[0]

            if 'customer_id' in error_info:
                raise InvalidCustomer
            elif 'payment_processor_information_id' in error_info:
                raise InvalidPaymentProcessorInformation
            else:
                raise err
        finally:
            db.session.rollback()

        return payment_method
