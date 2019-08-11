from flask import Flask, render_template, request
import sqlite3, pymysql,time
import sqlite_def as db 
import crawling_web as cr
from bs4 import BeautifulSoup
import urllib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route('/')
def index():    
    import crawling_selenium
    return render_template("index.html")

@app.route('/Movie_Project.html')
def Movie_Project():
    conn=pymysql.connect(host='127.0.0.1',
    port=3306,
    user='root',
    password='1234',
    db='movie',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)

    try:
        with conn.cursor() as cursor:
            sql="select * from current_movie" 
            cursor.execute(sql)
            movieList=cursor.fetchall()
    finally:
        conn.close()
    
    return render_template("Movie_Project.html",movieList=list(movieList))


# Movie Detail
@app.route('/movie_detail/<m_no>/<current_movie_title>')
def detail(m_no,current_movie_title):
    
    conn=pymysql.connect(host='127.0.0.1',
    port=3306,
    user='root',
    password='1234',
    db='movie',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)

    try:
        with conn.cursor() as cursor:
            sql='select * from current_movie c inner join test t on c.current_movie_title = t.title where current_movie_title = %s;'
            cursor.execute(sql,(current_movie_title))
            result=cursor.fetchone() # Bring only one element

            sql='select * from current_movie where current_movie_title = %s;'
            cursor.execute(sql,(current_movie_title))
            result1=cursor.fetchone() # Bring only one element

            sql='select * from board where m_no= %s;'
            cursor.execute(sql,(m_no))
            board=cursor.fetchall()
    finally:
        conn.close()
    if result is not None:    
        tmrvl=[]
        movieName = result['codem']

        for page in range(1,200):
            url="https://movie.naver.com/movie/bi/mi/review.nhn?code="+str(movieName)+"&page="+str(page)
            response = urllib.request.urlopen(url)

            soup=BeautifulSoup(response,'html.parser')
            table=soup.select('ul.rvw_list_area li a')
            for result3 in table:
                mrv=str(result3.string)
                tmrv=tuple([mrv])
                tmrvl.append(tmrv)
        df=pd.DataFrame(tmrvl)

    return render_template('movie_detail.html', board=board, movieInfo=result1)
    

@app.route('/KNN_Project.html')
def KNN_Project():
    return render_template("KNN_Project.html")

@app.route('/Contact.html')
def Contact():
    return render_template("Contact.html")

@app.route('/Project_Outline.html')
def Project_Outline():
    return render_template("Project_Outline.html")

@app.route('/QandA/', methods=['POST'])
def login():
    # Using sqlite3 instead of the MariaDB
    result = request.form.to_dict()

    # Create DB table for Q&A
    db.create_table()

    # Insert into table
    db.insert_QandA(result)

    # The probleme of the security, I'll add this service after... 
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    # Cheack code for the datas
#    db.all_QandA 
# in here i had to add smtp function 


#####
    return render_template("index.html")

@app.route('/ing.html')
def ing():
    db.create_movie_table()
    list_data = cr.crawling_cine() 

    for i in range(len(list_data)):
        trans_data = []
        trans_data.append(list_data[i]['num'])
        trans_data.append(list_data[i]['score'])
        trans_data.append(list_data[i]['title'])
        trans_data.append(list_data[i]['opinion'])
        trans_data.append(list_data[i]['author'])
        trans_data.append(list_data[i]['date'])
        db.insert_movies(trans_data)   
        #db.delete_cine()
    return render_template("Movie_Project.html")

@app.route('/delete.html')
def delete():
    db.delete_cine()
    return render_template("Movie_Project.html")

@app.route('/result_movies')
def result_movies():
    return render_template("result_movies.html")

@app.route('/test', methods=["post"])
def test():
    set_data = request.form.getlist('chk_info')
    print(set_data)
    year = set_data[0]
    set_data = set_data[1:]

    # load Data
    df_data_2000 = pd.read_csv('/home/ubuntu/portfolio/static/film_Data/film_'+str(year)+'.csv',index_col=None)

   # /home/ubuntu/portofolio/static/film_Data

    # 이름이 같은 영화들 데이터 합쳐 버리기
    df_data_2000_suc=df_data_2000.groupby('title').sum()

    # title을 인덱스에서 꺼내기 
    # [a,b,c] --> [a,b,c,title]
    df_data_2000_suc['title']=df_data_2000_suc.index

    #columns = ['a','b','c','title']
    columns=list(df_data_2000_suc.columns)

    # [분류범주]
    # title들을 리스트로 만들기
    # title_list = ['영화이름','영화이름','영화이름','영화이름','영화이름',...]
    title_list =[]
    title_list=list(df_data_2000_suc['title'])

    # [분류집단]
    df_data_2000_suc= df_data_2000_suc.iloc[:,0:25]  # usage = 0 : 25 = 왜냐하면 0부터 25번째 컬럼까지 0||1 의 데이터가 들어있기 때문에
    # From DataFrame to NumpyArray
    np_df_data_2000_suc=df_data_2000_suc.to_numpy()
    print(np_df_data_2000_suc)

    # [분류대상] for cinemas

    # <테스트용>
    #target = [0,1,0,0,1,
    #        0,0,0,0,0,
    #        1,0,0,0,0,
    #        0,0,0,0,0,
    #        0,0,0,0,0]

    genres = {'drama':0,'fantasy':0,'western':0,'horror':0,'romance':0,'adventure':0,'thriller':0,'noir':0,'cult':0,'documentary':0,'comedic':0,
    'family':0,'mystery':0,'war':0,'animation':0,'crime':0,'musical':0,'SF':0,'action':0,'heroism':0,'sexual':0,'suspense':0,
    'epic':0,'blackcomedic':0,'experiment':0}

    for i in set_data:
        for j in genres.keys():
            if i==j:
                genres[j] += 1
            else:
                pass
        target = list(genres.values()) 

    # KNN 시작
    def data_set():
        # 분류집단
        dataset = np.array(np_df_data_2000_suc) 
        size = len(dataset)

        # 분류대상
        # https://docs.scipy.org/doc/numpy/reference/generated/numpy.tile.html
        class_target = np.tile(target,(size,1))
        
        # 분류범주
        class_category = np.array(title_list)

        return dataset, class_target, class_category

    # dataset 생성
    dataset, class_target, class_category = data_set()

    def classify(dataset, class_target, class_category, k):
        # 유클리드 거리 계산
        diffMat = class_target - dataset    # 두 점의 차
        sqDiffMat = diffMat**2              # 차에 대한 제곱
        row_sum = sqDiffMat.sum(axis=1)     # 차에 대한 제급에 대한 합
        distance = np.sqrt(row_sum)         # 차에 대한 제곱에 대한 합의 제곱근(최종거리)

        # 가까운 거리 오름차순 정렬
        sortDist = distance.argsort()

        # 이웃한 k개 선정
        class_result={}
        for i in range(k):
            c = class_category[sortDist[i]]
            class_result[c] = class_result.get(c,0) + 1
        
        return class_result

    # 함수 호출 = 시작포인트
    k = 10
    class_result = classify(dataset, class_target, class_category, k)

    movies = [] 
    # 분류결과 출력 함수 정의
    def classify_result(class_result):
        for title in title_list:
            for recommand in class_result.keys():
                if recommand == title:
                    movies.append(title)
                else:
                    pass

    classify_result(class_result)

    return render_template('test.html',movies=movies, year=year)


if __name__ == '__main__':  
    app.run(host='0.0.0.0',port=5000, debug=True)
