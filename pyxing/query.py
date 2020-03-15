import win32com.client
import pythoncom
from pyxing import res
import pandas


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
        self.res = None

    def register_res(self, res_file):
        res_path = "C:\\eBEST\\xingAPI\\Res\\" + res_file
        self.res = res_file[:-4]
        self.received = False
        self.com_obj.ResFileName = res_path

    def set_field_data(self, field, data, index=0):
        block = self.res + "InBlock"
        self.com_obj.SetFieldData(block, field, index, data)

    def request(self, occurs=False, block=True):
        self.com_obj.Request(occurs)
        if block:
            while not self.received:
                pythoncom.PumpWaitingMessages()

    def get_field_data(self, field, index=0):
        block = self.res + "OutBlock"
        data = self.com_obj.GetFieldData(block, field, index)
        return data

    def get_block_count(self, block_name):
        return self.com_obj.GetBlockCount(block_name)

    def block_request(self, *args, **kwargs):
        res_name = args[0]
        res_file = res_name + ".res"
        res_path = "C:\\eBEST\\xingAPI\\Res\\" + res_file
        self.register_res(res_file)

        # set input
        for k in kwargs:
            self.set_field_data(k, kwargs[k])

        # request
        self.request()

        # parse res file
        f = open(res_path, encoding="euc-kr")
        res_lines = f.readlines()
        f.close()

        res_data = res.parse_res(res_lines)
        outblock_field = res_data['outblock_field']
        data = []
        rows = self.get_block_count(res_data['outblock'])

        for i in range(rows):
            elem = {k: self.get_field_data(k, i) for k in outblock_field}
            data.append(elem)

        df = pandas.DataFrame(data=data)
        return df


if __name__ == "__main__":
    # 로그인 정보
    f = open("../account.txt", "rt")
    lines = f.readlines()
    id = lines[0].strip()
    password = lines[1].strip()
    cert = lines[2].strip()
    f.close()

    # 로그인
    from pyxing import session

    # Session
    xasession = session.XASession()
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


