from pyxing.session import *

f = open("account.txt", "rt")
lines = f.readlines()
id = lines[0].strip()
password = lines[1].strip()
cert = lines[2].strip()
f.close()

xasession = XASession()
xasession.login(id, password, cert, block=True)

print("서버이름: ", xasession.get_server_name())
print("연결상태: ", xasession.is_connected())
print("계좌수  : ", xasession.get_account_list_count())
print("계좌    : ", xasession.get_account_list(0))
