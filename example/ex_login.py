from pyxing.session import *

f = open("../account.txt", "rt")            # 계정 정보 파일 열기
lines = f.readlines()                       # 파일에서 모든 라인 읽기
id = lines[0].strip()                       # 첫번째 라인의 데이터 (아이디)
password = lines[1].strip()                 # 두번째 라인의 데이터 (패스워드)
cert = lines[2].strip()                     # 세번째 라인의 데이터 (공인인증서)
f.close()

xasession = XASession(type=1)               # 0: 실서버, 1: 모의서버, 2: xingACE
xasession.login(id, password, cert, block=True)

print("서버이름: ", xasession.get_server_name())
print("연결상태: ", xasession.is_connected())
print("계좌수  : ", xasession.get_account_list_count())
print("계좌    : ", xasession.get_account_list(0))