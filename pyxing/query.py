import win32com.client
import pythoncom


class XAQueryEvents:
    def __init__(self):
        self.com_obj = None                 # COM 객체
        self.user_obj = None                # 사용자 클래스에 대한 객체

    def OnReceiveData(self, code):
        print(code)
        self.user_obj.received = True

    def connect(self, com_obj, user_obj):
        """
        객체끼리 서로 연결하는 메서드
        :param com_obj: COM 객체
        :param user_obj: 사용자 클래스에 대한 객체
        :return:
        """
        self.com_obj = com_obj
        self.user_obj = user_obj


class XAQuery:
    def __init__(self):
        self.com_obj = win32com.client.Dispatch("XA_DataSet.XAQuery")                     # COM 객체 생성
        self.event_handler = win32com.client.WithEvents(self.com_obj, XAQueryEvents)      # 이벤트 처리 클래스 연결
        self.event_handler.connect(self.com_obj, self)
        self.received = False

    def register_res(self, res):
        res_path = "C:\\eBEST\\xingAPI\\Res\\" + res
        print(res_path)
        self.com_obj.ResFileName = res_path

    def set_field_data(self, block, field, data, index=0):
        self.com_obj.SetFieldData(block, field, index, data)

    def request(self, occurs=False, block=True):
        self.com_obj.Request(occurs)
        if block:
            while not self.received:
                pythoncom.PumpWaitingMessages()

    def get_field_data(self, block, field, index=0):
        data = self.com_obj.GetFieldData(block, field, index)
        return data


if __name__ == "__main__":
    # 로그인
    from pyxing import session

    # Session
    xasession = session.XASession()
    xasession.login("id", "password", "cert", block=True)

    # Query
    xaquery = XAQuery()
    xaquery.register_res("t1102.res")
    xaquery.set_field_data("t1102InBlock", "shcode", "039490")
    xaquery.request()

    name = xaquery.get_field_data("t1102OutBlock", "hname")
    price = xaquery.get_field_data("t1102OutBlock", "price")
    print(name, price)


