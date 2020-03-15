from pyxing.session import *
from pyxing.query import *

# 계정정보
f = open("account.txt", "rt")
lines = f.readlines()
id = lines[0].strip()
password = lines[1].strip()
cert = lines[2].strip()
f.close()

# login
xasession = XASession()
xasession.login(id, password, cert, block=True)

# Query
xaquery = XAQuery()
xaquery.register_res("t1102.res")
xaquery.set_field_data("shcode", "039490")
xaquery.request()

name = xaquery.get_field_data("hname")
price = xaquery.get_field_data("price")
print(name, price)


# block request
df = xaquery.block_request("t8430", gubun=0)
print(df)
df.to_excel("code.xlsx")
