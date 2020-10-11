from datetime import datetime
import uuid
from sqlalchemy import Column, String, ForeignKey
import sqlalchemy.dialects.postgresql as postgresql
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.exc import IntegrityError

from primer import db
from primer.exceptions import InvalidCustomer

class PaymentProcessorCustomerInformation(db.Model):
    __tablename__ = 'payment_processor_customer_informations'
    id = Column(postgresql.UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    information = Column(MutableDict.as_mutable(postgresql.JSONB), nullable=False)
    customer_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('customers.id'), nullable=False)
    created_at = Column(postgresql.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(postgresql.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)

    @classmethod
    def create(kls, name: str, customer, information: dict):
        payment_processor_customer_information = PaymentProcessorCustomerInformation(
            name = name,
            customer_id = customer.id,
            information = information
        )

        try:
            db.session.add(payment_processor_customer_information)
            db.session.commit()
        except IntegrityError as err:
            error_info = err.orig.args[0]

            if 'customer_id' in error_info:
                raise InvalidCustomer
            else:
                raise err
        finally:
            db.session.rollback()

        return payment_processor_customer_information

    @classmethod
    def find_by_id(kls, id: uuid.UUID):
        return PaymentProcessorCustomerInformation.query.filter_by(
            id = id
        ).first()

    @classmethod
    def find_by_customer_id_and_processor_name(kls, id: uuid.UUID, name: str):
        return PaymentProcessorCustomerInformation.query.filter_by(
            customer_id = id,
            name = name,
        ).first()
