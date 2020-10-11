from primer.models.payment_processor_customer_information import PaymentProcessorCustomerInformation

class PaymentProcessorCustomerInformationCreate:
    def __init__(self, processor_name: str, customer, information: dict):
        self.processor_name = processor_name
        self.customer = customer
        self.information = information

    def create_payment_processor_customer_information(self):
        customer_information = PaymentProcessorCustomerInformation.find_by_customer_id_and_processor_name(
            self.customer.id,
            self.processor_name
        )

        if customer_information is None:
            customer_information = PaymentProcessorCustomerInformation.create(
                self.processor_name,
                self.customer,
                self.information
            )

        return customer_information


    @classmethod
    def call(kls, processor_name: str, customer, information: dict):
        customer_information = kls(processor_name, customer, information)

        return customer_information.create_payment_processor_customer_information()


