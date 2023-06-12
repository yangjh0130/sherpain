from tenable.io import TenableIO
import sys
from openpyxl import load_workbook
import time 

# 1. 접속 정보 입력 : TenableIO('ACCESS_KEY', 'SECRET_KEY')
tio = TenableIO('fdd54b09821269953a71e908623f0eb5f8b2007b2b8ef6d8371eddde6cc8e776', '206df45036eb236de0985bc6b192cec3b5f098320ec6c36e41a5173cfff3815f')

file_path = "C:/Users/YJH/Desktop/python/tenable/asset_tag/AddAsset.xlsx"

# 엑셀파일 읽어오기
load_wd = load_workbook(file_path, data_only=True)
load_ws=load_wd['Sheet1']

# 데이터 읽어 오기
data = []
for row in load_ws.rows:
    data.append([row[0].value, row[1].value,row[2].value])

# 번호        : data[1][0], 
# IP 주소     : data[1][1]
# TAG Value : data[1][2] 
# 예시data[5][2] 5번째줄 3번째 칸


num=len(data)
num = 0

print("=============== Asset 등록을 시작 합니다.==========================")
print("")
for i, j, k in data:
    #ipaddr=data[i][1]
    assetip=[]
    ipdict={}
    assetip.append(j)
    ipdict={'ipv4':assetip}
    respon=tio.assets.asset_import('static', ipdict)
    print(respon)
    print(  str(num+1) + "..         IP 주소 :"+ j + "      등록 완료") 
    num+=1

    # 2. TAG 이름 검색 후 UUID 확인
    tuuid=[]
    for tag in tio.tags.list(('value', 'eq', k )):
        tuuid.append(tag['uuid'])
        print(k +"의 TAG UUID 확인")

    n=0
    m=0
    aid=[]
    while True:
        m+=1
        try:             
            for asset in tio.assets.list():
                if j == asset['ipv4'][0] :
                    aid.append(asset['id'])
                    n=1
                    break   
        except IndexError as e:   
            if m==1 :     
                print("Asset 등록 중")
                continue
    
            if m!=1:
                print(".")
                time.sleep(10)
                continue
        if n==1 :
            break
    print(j, "의 Asset UUID : ", aid)

    tio.tags.assign(aid,tuuid)
    print("Asset에 Tag 할당 완료")

print(" ")    
print("--------------------------------------------------------------------------")
print("     "+str(num)   + " 개 등록 완료")
print(" ")
print(" ")
print(" ")
