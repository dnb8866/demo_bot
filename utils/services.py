import asyncio
import decimal
import hashlib
import uuid
import var_dump as var_dump


from urllib import parse
from urllib.parse import urlparse
from yookassa import Payment, Configuration


class Robokassa:

    @staticmethod
    def parse_response(request: str) -> dict:
        """
        :param request: Link.
        :return: Dictionary.
        """
        params = {}

        for item in urlparse(request).query.split('&'):
            key, value = item.split('=')
            params[key] = value
        return params

    def calculate_signature(*args) -> str:
        """Create signature MD5.
        """
        return hashlib.md5(':'.join(str(arg) for arg in args).encode()).hexdigest()

    def check_signature_result(
            self,
            order_number: int,  # invoice number
            received_sum: decimal,  # cost of goods, RU
            received_signature: hex,  # SignatureValue
            password: str  # Merchant password
    ) -> bool:
        signature = self.calculate_signature(received_sum, order_number, password)
        if signature.lower() == received_signature.lower():
            return True
        return False

    def generate_payment_link(
            self,
            merchant_login: str,  # Merchant login
            merchant_password_1: str,  # Merchant password
            cost: decimal,  # Cost of goods, RU
            number: int,  # Invoice number
            description: str,  # Description of the purchase
            is_test=0,
            robokassa_payment_url='https://auth.robokassa.ru/Merchant/Index.aspx',
    ) -> str:
        """URL for redirection of the customer to the service.
        """
        signature = self.calculate_signature(
            merchant_login,
            cost,
            number,
            merchant_password_1
        )

        data = {
            'MerchantLogin': merchant_login,
            'OutSum': cost,
            'InvId': number,
            'Description': description,
            'SignatureValue': signature,
            'IsTest': is_test
        }
        return f'{robokassa_payment_url}?{parse.urlencode(data)}'

    def result_payment(self, merchant_password_2: str, request: str) -> str:
        """Verification of notification (ResultURL).
        :param merchant_password_2:
        :param request: HTTP parameters.
        """
        param_request = self.parse_response(request)
        cost = param_request['OutSum']
        number = param_request['InvId']
        signature = param_request['SignatureValue']

        if self.check_signature_result(number, cost, signature, merchant_password_2):
            return f'OK{param_request["InvId"]}'
        return "bad sign"

    def check_success_payment(self, merchant_password_1: str, request: str) -> str:
        """ Verification of operation parameters ("cashier check") in SuccessURL script.
        :param merchant_password_1:
        :param request: HTTP parameters
        """
        param_request = self.parse_response(request)
        cost = param_request['OutSum']
        number = param_request['InvId']
        signature = param_request['SignatureValue']

        if self.check_signature_result(number, cost, signature, merchant_password_1):
            return "Thank you for using our service"
        return "bad sign"


class Yookassa:
    Configuration.account_id = '506751'
    Configuration.secret_key = '538350'

    @staticmethod
    async def create():
        payment = Payment.create(
            {
                "amount": {
                    "value": 1000,
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": "https://merchant-site.ru/return_url"
                },
                "capture": True,
                "description": "Заказ №72",
                "metadata": {
                    'orderNumber': '72'
                },
                "receipt": {
                    "customer": {
                        "full_name": "Ivanov Ivan Ivanovich",
                        "email": "email@email.ru",
                        "phone": "79211234567",
                        "inn": "6321341814"
                    },
                    "items": [
                        {
                            "description": "Переносное зарядное устройство Хувей",
                            "quantity": "1.00",
                            "amount": {
                                "value": 1000,
                                "currency": "RUB"
                            },
                            "vat_code": "2",
                            "payment_mode": "full_payment",
                            "payment_subject": "commodity",
                            "country_of_origin_code": "CN",
                            "product_code": "44 4D 01 00 21 FA 41 00 23 05 41 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 12 00 AB 00",
                            "customs_declaration_number": "10714040/140917/0090376",
                            "excise": "20.00",
                            "supplier": {
                                "name": "string",
                                "phone": "string",
                                "inn": "string"
                            }
                        },
                    ]
                }
            }
        )

        var_dump.var_dump(payment)

        # get confirmation url
        confirmation_url = payment.confirmation.confirmation_url

        print(payment)

        print(confirmation_url)
        #
        # while True:
        #     if payment.status == 'pending':
        #         await asyncio.sleep(5)
        #     else:
        #         return 'Оплата прошла успешно'

