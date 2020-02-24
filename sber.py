import requests
import json
#getOrderStatusExtended.do
login = 'r-tango-api'
password = 'r-tango'
# response = requests.get('https://3dsec.sberbank.ru/payment/rest/register.do?'
#                         'amount=100&'
#                         'currency=643&'
#                         'language=ru&'
#                         'orderNumber=12j9p34&'
#                         'description=оплата заказа 100&'
#                         'password=r-tango&'
#                         'userName=r-tango-api&'
#                         'returnUrl=http://localhost:8000/success&'
#                         'failUrl=http://localhost:8000/fail&'
#                         'pageView=DESKTOP&sessionTimeoutSecs=1200',)
response = requests.get('https://3dsec.sberbank.ru/payment/rest/getOrderStatusExtended.do?'
                        'orderId=88185de2-f847-7917-abfc-fe7a5e3032ec&'                       
                        'language=ru&'
                        'orderNumber=43947879&'                       
                        'password=r-tango&'
                        'userName=r-tango-api&'
                        )
print(json.loads(response.content))
response_data = json.loads(response.content)

