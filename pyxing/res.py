# RES file parser
'''
{'trcode': "CSPAT00600",
 'inblock': [
    {'CSPAT00600InBlock1': [  ]}
 ],
 'outblock': [
    {'CSPAT00600OutBlock1': [  ]}
    {'CSPAT00600OutBlock2': [  ]}
 }
'''


# res 파일 정보 라인 파싱 함수
def parse_info(data):
    tokens = data.split(',')
    return tokens[2].strip()


# InBlock/OutBlock 파싱 함수
def parse_block(data):
    # block 코드, 타입
    block_info = data[0]
    tokens = block_info.split(",")
    block_code, block_type = tokens[0], tokens[-1][:-1]

    # block fields
    field_codes = []
    fields = data[2:]

    for line in fields:
        if len(line) > 0:
            field_code = line.split(',')[1].strip()
            field_codes.append(field_code)

    ret_data = {}
    ret_data[block_code] = field_codes
    return block_type, ret_data


def parse_res(lines):
    lines = [line.strip() for line in lines]

    info_index = [i for i,x in enumerate(lines) if x.startswith((".Func", ".Feed"))][0]
    begin_indices = [i-1 for i,x in enumerate(lines) if x == "begin"]
    end_indices = [i for i,x in enumerate(lines) if x == "end"]
    block_indices = zip(begin_indices, end_indices)

    ret_data = {"trcode": None, "inblock": [], "outblock": []}

    # TR Code
    tr_code = parse_info(lines[info_index])
    ret_data["trcode"] = tr_code

    # Block
    for start, end in block_indices:
        block_type, block_data= parse_block(lines[start:end])
        if block_type == "input":
            ret_data["inblock"].append(block_data)
        else:
            ret_data["outblock"].append(block_data)

    return ret_data


if __name__ == "__main__":
    # TR(t8340)
    f = open("c:/eBEST/xingAPI/Res/t8430.res", encoding="euc-kr")
    lines = f.readlines()
    f.close()

    # f = open("c:/eBEST/xingAPI/Res/CSPAT00600.res", encoding="euc-kr")
    # lines = f.readlines()
    # f.close()

    # Real
    #f = open("c:/eBEST/xingAPI/Res/NWS.res", encoding="euc-kr")
    #lines = f.readlines()
    #f.close()

    import pprint
    data = parse_res(lines)
    pprint.pprint(data)


