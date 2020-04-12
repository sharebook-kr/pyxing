from pyxing.session import *
from pyxing.query import *

# 계정정보
f = open("../account.txt", "rt")
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

# 직접 요청하기
xaquery.register_res("t1102.res")
xaquery.set_field_data("t1102InBlock", "shcode", "039490")
xaquery.request()

name = xaquery.get_field_data("t1102OutBlock", "hname")
price = xaquery.get_field_data("t1102OutBlock", "price")
print(name, price)


# block request
dfs = xaquery.block_request("t8430", gubun=0)
print(dfs[0])
dfs[0].to_excel("code.xlsx")
