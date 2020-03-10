from pyxing.session import *
from pyxing.query import *

# login
xasession = XASession()
xasession.login("id", "password", "cert", block=True)

# Query
xaquery = XAQuery()
xaquery.register_res("t1102.res")
xaquery.set_field_data("t1102InBlock", "shcode", "039490")
xaquery.request()

name = xaquery.get_field_data("t1102OutBlock", "hname")
price = xaquery.get_field_data("t1102OutBlock", "price")
print(name, price)


