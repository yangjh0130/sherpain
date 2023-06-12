from tenable.io import TenableIO
from openpyxl import load_workbook

########################################################
#                                                      #
#                                                      #
#         asset_file_path, tio 정보 수정 후 실행        #
#                                                      #
#                                                      #
########################################################


# Asset 엑셀 파일 경로
asset_file_path = "C:/Users/YJH/Desktop/python/tenable/asset_tag/AddAsset.xlsx"

# 접속 정보 입력 : Tenable.IO('ACCESS_KEY', 'SECRET_KEY')
tio = TenableIO('3210fd3958dd5243fa4580dc5e088fd4bf2a6739896ff28b1de4ea567ed3dd54', 'cd95b22df1da6d80c5e5b4ce52a257f279ecf7825f45aa7f6c313863623c98a2')

# asset에 tag 설정
def set_tag():

    # 엑셀파일 읽어오기
    load_wd = load_workbook(asset_file_path, data_only=True)
    load_ws=load_wd['Sheet1']

    # 데이터 읽어 오기
    data = []
    for row in load_ws.rows:
        data.append([row[1].value, row[2].value, row[3].value])
    
    num=0
    print("========================== Asset에 Tag 등록을 시작합니다. ==========================")

    # value 검색 후 UUID 확인
    for i, j, k in data:

        for asset in tio.assets.list():
            if (str(asset['ipv4'])) == "['"+i+"']":
                asset_uuid = (asset['id'])
    
        for tag in tio.tags.list():
            if tag['value'] == k:
                value_uuid = tag['uuid']

                # tag 설정
                tio.tags.assign(assets=[asset_uuid], tags=[value_uuid])

                print(str(num+1) + "..         "+"Asset: "+i+ " Tag 등록 완료")
                num+=1

    print("========================== Asset에 Tag 등록이 완료되었습니다. ==========================")

set_tag()
