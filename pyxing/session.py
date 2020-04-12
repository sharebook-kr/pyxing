import win32com.client
import pythoncom


class XASessionEvents:
    def __init__(self):
        self.com_obj = None                 # COM 객체
        self.user_obj = None                # 사용자 클래스에 대한 객체

    def OnLogin(self, code, msg):
        """
        서버와의 로그인이 끝나면 발생하는 이벤트
        :param code: 서버에서 받은 메시지 코드
        :param msg: 서버에서 받은 메시지 정보
        :return:
        """
        if code == '0000':
            self.user_obj.connected = True

    def connect(self, com_obj, user_obj):
        """
        객체끼리 서로 연결하는 메서드
        :param com_obj: COM 객체
        :param user_obj: 사용자 클래스에 대한 객체
        :return:
        """
        self.com_obj = com_obj
        self.user_obj = user_obj


class XASession:
    def __init__(self, type=0):
        self.com_obj = win32com.client.Dispatch("XA_Session.XASession")                     # COM 객체 생성
        self.event_handler = win32com.client.WithEvents(self.com_obj, XASessionEvents)      # 이벤트 처리 클래스 연결
        self.event_handler.connect(self.com_obj, self)

        self.connected = False
        self._connect_server(type)

    def _connect_server(self, type):
        if type == 0:
            server = "hts.ebestsec.co.kr"
        elif type == 1:
            server = "demo.ebestsec.co.kr"
        else:
            server = "127.0.0.1"

        self.com_obj.ConnectServer(server, 20001)

    def login(self, id, password, cert, block=True):
        self.com_obj.Login(id, password, cert, 0, 0)

        # 로그인이 될 때까지 대기
        if block:
            while not self.connected:
                pythoncom.PumpWaitingMessages()

    def disconnect_server(self):
        """
        서버에 연결을 종료합니다.
        :return:
        """
        self.com_obj.DisconnectServer()

    def is_connected(self):
        connect = self.com_obj.IsConnected()
        return connect

    def get_account_list_count(self):
        count = self.com_obj.GetAccountListCount()
        return count

    def get_account_list(self, index):
        account = self.com_obj.GetAccountList(index)
        return account

    def get_account_name(self, number):
        name = self.com_obj.GetAccountName(number)
        return name

    def get_acct_detail_name(self, number):
        name = self.com_obj.GetAcctDetailName(number)
        return name

    def get_server_name(self):
        name = self.com_obj.GetServerName()
        return name


if __name__ == "__main__":
    # 로그인 정보
    f = open("../account.txt", "rt")
    lines = f.readlines()
    id = lines[0].strip()
    password = lines[1].strip()
    cert = lines[2].strip()
    f.close()

    # 객체 생성
    session = XASession(demo=True)
    session.login(id, password, cert, block=True)
    acc = session.get_account_list(0)
    print(acc)

