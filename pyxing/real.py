import pandas
import win32com.client
import pythoncom
from queue import Queue
from pyxing import res


class XARealEvents:
    def __init__(self):
        self.com_obj = None
        self.user_obj = None
        self.queue = None

    def OnReceiveRealData(self, trcode):
        res_data = self.user_obj.res.get(trcode)
        out_data = {}

        out_block = res_data['outblock'][0]

        for field in out_block['OutBlock']:
            data = self.user_obj.get_field_data(field)
            out_data[field] = data

        out_data_list = [out_data]
        df = pandas.DataFrame(data=out_data_list)
        self.queue.put((trcode, df))

    def connect(self, com_obj, user_obj, queue):
        self.com_obj = com_obj
        self.user_obj = user_obj
        self.queue = queue


class XAReal:
    def __init__(self, queue):
        self.com_obj = win32com.client.Dispatch("XA_DataSet.XAReal")                    # COM 객체 생성
        self.event_handler = win32com.client.WithEvents(self.com_obj, XARealEvents)     # 이벤트 처리 클래스 연결
        self.event_handler.connect(self.com_obj, self, queue)
        self.res = {}

    def register_res(self, res_file):
        """
        RES 파일 등록
        :param res_file: res 파일 (JIF.res)
        :return:
        """
        # Res 파일 등록
        res_name = res_file[:-4]
        res_path = "C:\\eBEST\\xingAPI\\Res\\" + res_file
        self.com_obj.ResFileName = res_path

        # Res 파일 파싱
        with open(res_path, encoding="euc-kr") as f:
            res_lines = f.readlines()
            res_data = res.parse_res(res_lines)
            self.res[res_name] = res_data

    def set_field_data(self, field, data):
        ret = self.com_obj.SetFieldData("InBlock", field, data)

    def advise_real_data(self):
        ret = self.com_obj.AdviseRealData()

    def get_field_data(self, field):
        data = self.com_obj.GetFieldData("OutBlock", field)
        return data

    def unadvise_real_data(self):
        """
        실시간 데이터 요청 취소
        :return:
        """
        self.com_obj.UnadviseRealData()


if __name__ == "__main__":
    from threading import Thread

    # 데이터를 소비하는 스레드
    def consumer(in_q):
        while True:
            data = in_q.get()
            print("consumer - trcode ", data[0])
            print("consumer - data ", data[1])


    # 로그인 정보
    f = open("../account.txt", "rt")
    lines = f.readlines()
    id = lines[0].strip()
    password = lines[1].strip()
    cert = lines[2].strip()
    f.close()

    # 로그인 (Session)
    from pyxing import session
    xasession = session.XASession()
    print("login requst")
    xasession.login(id, password, cert, block=True)
    print("login done")

    # Real 사용하기
    # 스레드간 데이터 전달을 위한 Queue 객체 생성하기
    queue = Queue()
    xareal = XAReal(queue)
    xareal.register_res("NWS.res")
    xareal.set_field_data("nwcode", "NWS001")
    xareal.advise_real_data()

    # 데이터를 소비하는 스레드 시작
    t2 = Thread(target=consumer, args=(queue,))
    t2.start()

    while True:
        pythoncom.PumpWaitingMessages()

