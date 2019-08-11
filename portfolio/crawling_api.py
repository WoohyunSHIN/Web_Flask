import urllib.request as ul
import json, datetime
import pandas as pd

# 시작 날짜 현재부터 2018년 초까지.
movieDate = "20190724"
cine=[{}]
# 매주 목요일 새로운 영화가 나오고 있던 이미있던 영화가 사라진다. 따라서 수요일을 기준으로한다.  
while int(movieDate)//10000 != 2018:
    url = f"http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key=a6c385f06167dbe3fd830bbe57d4ac65&targetDt={movieDate}"
    request = ul.Request(url)

    response = ul.urlopen(request)
    rescode = response.getcode()

    if(rescode == 200):
        responseData = response.read()

    result = json.loads(responseData)

    pre_result =result["boxOfficeResult"]
    pre_result1 = pre_result["dailyBoxOfficeList"]


    # 날짜, 영화이름, 누적관객수
    for i in range(0,len(pre_result1)):
        cine.append({"date":movieDate,"movieNm":pre_result1[i]["movieNm"],"audiAcc":pre_result1[i]["audiAcc"]})
    

    #반복 함수 마지막에 날짜를 줄이는 함수를 사용한다.
    #str -> date
    datetime_obj = datetime.datetime.strptime(movieDate,"%Y%m%d").date()
    # 1주일씩 시간을 줄여간다.
    datetime_obj_tmp = datetime_obj - datetime.timedelta(weeks=1)
    #date -> str
    day = datetime_obj_tmp.strftime("%Y-%m-%d").split('-')
    movieDate = day[0]+day[1]+day[2]
# 필요없는 리스트 없애기
del cine[0]

dataframe=pd.DataFrame(cine)
dataframe.to_csv("/home/ubuntu/portfolio/cine.csv")
print(dataframe)
print(type(dataframe))
