import win32com.client
import pythoncom
import threading


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
        print(code, msg)
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


class XASession(threading.Thread):
    def __init__(self, id, password, cert):
        super().__init__()

        self.id = id
        self.password = password
        self.cert = cert
        self.connected = False

    def run(self):
        # single threaded apartment
        pythoncom.CoInitialize()

        self.com_obj = win32com.client.Dispatch("XA_Session.XASession")
        self.event_handler = win32com.client.WithEvents(self.com_obj, XASessionEvents)
        self.event_handler.connect(self.com_obj, self)

        self._connect_server()          # 서버 연결
        self._login()                   # 로그인

        # 로그인이 될 때 까지 대기
        while not self.connected:
            pythoncom.PumpWaitingMessages()

        pythoncom.CoUninitialize()

    def _connect_server(self):
        self.com_obj.ConnectServer("hts.ebestsec.co.kr", 20001)

    def _login(self):
        self.com_obj.Login(self.id, self.password, self.cert, 0, 0)

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

    def login(self, blocking=True):
        """
        서버에 로그인합니다.
        :param blocking: True - 로그인 될 때까지 main thread blocking, False: main thread blocking 안됨
        :return:
        """
        self.start()
        if blocking:
            self.join()


if __name__ == "__main__":
    s = XASession("id", "passoword", "cert")
    s.login()
    acc = s.get_account_list(0)
    print(acc)

    while True:
        pythoncom.PumpWaitingMessages()

