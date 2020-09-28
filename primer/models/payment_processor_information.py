from datetime import datetime
import uuid
from sqlalchemy import Column, String
import sqlalchemy.dialects.postgresql as postgresql
from sqlalchemy.ext.mutable import MutableDict

from primer import db

class PaymentProcessorInformation(db.Model):
    __tablename__ = 'payment_processor_informations'
    id = Column(postgresql.UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    information = Column(MutableDict.as_mutable(postgresql.JSONB), nullable=False)
    created_at = Column(postgresql.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(postgresql.TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)

    @classmethod
    def create(kls, name: str, information: dict):
        payment_processor_information = PaymentProcessorInformation(
            name = name,
            information = information
        )

        db.session.add(payment_processor_information)
        db.session.commit()

        return payment_processor_information

    @classmethod
    def find_by_id(kls, id: uuid.UUID):
        return PaymentProcessorInformation.query.filter_by(
            id = id
        ).first()
