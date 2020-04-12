import win32com.client
import pythoncom
from pyxing import res
import pandas


class XAQueryEvents:
    def __init__(self):
        self.com_obj = None                 # COM 객체
        self.user_obj = None                # 사용자 클래스에 대한 객체

    def OnReceiveData(self, code):
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
        self.com_obj = win32com.client.Dispatch("XA_DataSet.XAQuery")                   # COM 객체 생성
        self.event_handler = win32com.client.WithEvents(self.com_obj, XAQueryEvents)    # 이벤트 처리 클래스 연결
        self.event_handler.connect(self.com_obj, self)
        self.received = False

    def register_res(self, res_file):
        res_path = "C:\\eBEST\\xingAPI\\Res\\" + res_file       # res file 기본 경로
        self.received = False                                   # res file이 등록된 경우 received 상태 초기화
        self.com_obj.ResFileName = res_path                     # res file 등록

    def set_field_data(self, block_code, field, data, index=0):
        self.com_obj.SetFieldData(block_code, field, index, data)

    def request(self, occurs=False, block=True):
        self.com_obj.Request(occurs)
        if block:
            while not self.received:
                pythoncom.PumpWaitingMessages()

    def get_field_data(self, block_code, field, index=0):
        data = self.com_obj.GetFieldData(block_code, field, index)
        return data

    def get_block_count(self, block_name):
        return self.com_obj.GetBlockCount(block_name)

    def block_request(self, *args, **kwargs):
        res_name = args[0]
        res_file = res_name + ".res"
        res_path = "C:\\eBEST\\xingAPI\\Res\\" + res_file
        self.register_res(res_file)

        # res 파일 파싱
        with open(res_path, encoding="euc-kr") as f:
            res_lines = f.readlines()
        res_data = res.parse_res(res_lines)

        inblock_code = list(res_data['inblock'][0].keys())[0]
        inblock_field = list(res_data['inblock'][0].values())[0]

        # set input
        for k in kwargs:
            self.set_field_data(inblock_code, k, kwargs[k])
            if k not in inblock_field:
                print("inblock field error")
            print(inblock_code, k, kwargs[k])

        # request
        self.request()

        print("request ok")
        ret = []
        for outblock in res_data['outblock']:
            outblock_code = list(outblock.keys())[0]
            outblock_field = list(outblock.values())[0]

            data = []
            rows = self.get_block_count(outblock_code)
            for i in range(rows):
                elem = {k: self.get_field_data(outblock_code, k, i) for k in outblock_field}
                data.append(elem)

            df = pandas.DataFrame(data=data)
            ret.append(df)
        return ret


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

    # Query setting
    xaquery = XAQuery()

    #xaquery.register_res("t1102.res")
    #xaquery.set_field_data("t1102InBlock", "shcode", "039490")
    #xaquery.request()
    #name = xaquery.get_field_data("t1102OutBlock", "hname")
    #price = xaquery.get_field_data("t1102OutBlock", "price")
    #print(name, price)

    # block request
    dfs = xaquery.block_request("t8430", gubun=0)
    print(dfs[0])
    df = dfs[0]
    df.to_excel("code.xlsx")


