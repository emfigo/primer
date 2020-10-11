from datetime import datetime
import uuid
from sqlalchemy import Column, String, ForeignKey
import sqlalchemy.dialects.postgresql as postgresql
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.exc import IntegrityError

from primer import db
from primer.exceptions import InvalidCustomer

class PaymentProcessorPaymentInformation(db.Model):
    __tablename__ = 'payment_processor_payment_informations'
    id = Column(postgresql.UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    information = Column(MutableDict.as_mutable(postgresql.JSONB), nullable=False)
    payment_method_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('payment_methods.id'), nullable=False)
    created_at = Column(postgresql.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(postgresql.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)

    @classmethod
    def create(kls, name: str, payment_method, information: dict):
        payment_processor_payment_information = PaymentProcessorPaymentInformation(
            name = name,
            payment_method_id = payment_method.id,
            information = information
        )

        try:
            db.session.add(payment_processor_payment_information)
            db.session.commit()
        except IntegrityError as err:
            error_info = err.orig.args[0]

            if 'payment_method_id' in error_info:
                raise InvalidPaymentMethod
            else:
                raise err
        finally:
            db.session.rollback()

        return payment_processor_payment_information

    @classmethod
    def find_by_id(kls, id: uuid.UUID):
        return PaymentProcessorPaymentInformation.query.filter_by(
            id = id
        ).first()

    @classmethod
    def find_by_payment_method_id_and_processor_name(kls, payment_method_id: uuid.UUID, name: str):
        return PaymentProcessorPaymentInformation.query.filter_by(
            payment_method_id = payment_method_id,
            name = name
        ).first()
