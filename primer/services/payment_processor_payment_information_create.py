from primer.models.payment_processor_payment_information import PaymentProcessorPaymentInformation

class PaymentProcessorPaymentInformationCreate:
    def __init__(self, processor_name: str, payment_method, information: dict):
        self.processor_name = processor_name
        self.payment_method = payment_method
        self.information = information

    def create_payment_processor_payment_information(self):
        payment_information = PaymentProcessorPaymentInformation.find_by_payment_method_id_and_processor_name(
            self.payment_method.id,
            self.processor_name
        )

        if payment_information is None:
            payment_information = PaymentProcessorPaymentInformation.create(
                self.processor_name,
                self.payment_method,
                self.information
            )

        return payment_information


    @classmethod
    def call(kls, processor_name: str, payment_method, information: dict):
        payment_information = kls(processor_name, payment_method, information)

        return payment_information.create_payment_processor_payment_information()

