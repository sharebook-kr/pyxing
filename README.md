# pyxing
이베스트투자증권 xing API python wrapper 

## 로그인

```python
from pyxing.session import *

xasession = XASession()
xasession.login("아이디", "비밀번호", "공인인증비밀번호", block=True)

print("서버이름: ", xasession.get_server_name())
print("연결상태: ", xasession.is_connected())
print("계좌수  : ", xasession.get_account_list_count())
print("계좌    : ", xasession.get_account_list(0))
```

## TR 요청 (블록킹)

XAQuery 클래스는 block_request()라는 블록킹 기반의 TR 요청 메서드를 제공합니다. 여기서 블록킹(blocking)의 의미는 서버로부터 TR 데이터를 받을 때까지 대기함을 의미합니다. 

```python
from pyxing.session import *
from pyxing.query import *

# login
xasession = XASession()
xasession.login("아이디", "비밀번호", "공인인증비밀번호", block=True)

# block request
xaquery = XAQuery()
df = xaquery.block_request("t8430", gubun=0)
print(df)
#df.to_excel("code.xlsx")
```
