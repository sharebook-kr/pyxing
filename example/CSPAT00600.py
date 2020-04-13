from pyxing.session import *
from pyxing.query import *

# 로그인 정보 불러오기
f = open("../account.txt", "rt")
lines = f.readlines()
id = lines[0].strip()
password = lines[1].strip()
cert = lines[2].strip()
f.close()

# 로그인
xasession = XASession(type=2)
xasession.login(id, password, cert, block=True)

# CSPAT00600 TR 요청
xaquery = XAQuery()
dfs = xaquery.block_request("CSPAT00600",
                            AcntNo="계좌번호",
                            InptPwd="비밀번호",
                            IsuNo="005930",
                            OrdQty=2,
                            OrdPrc=40000,
                            BnsTpCode="2",
                            OrdprcPtnCode="00",
                            MgntrnCode="000",
                            LoanDt="0",
                            OrdCndiTpCode="0")
print(dfs)


