import sqlite3

# CREATE table
def create_table():
    conn = sqlite3.connect('/home/ubuntu/portfolio/static/sqlite3/QandA.db')
    cursor=conn.cursor()
    cursor.execute('''CREATE TABLE if not exists QandAs(
        email text,
        context text
    )''')
    conn.commit()
    conn.close()

# INSERT data
def insert_QandA(items):
    conn = sqlite3.connect('/home/ubuntu/portfolio/static/sqlite3/QandA.db')
    cursor = conn.cursor()

    sql = 'INSERT INTO QandAs VALUES(?,?)'
    target = [items['email'],items['context']]
    cursor.execute(sql,target)
    conn.commit()
    conn.close()

# Print all
def all_QandA():
    conn=sqlite3.connect('/home/ubuntu/portfolio/static/sqlite3/QandA.db')
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM QandAs")
    print('[1] 전체 데이터 출력하기')
    QandAs=cursor.fetchall()

    for QandA in QandAs:
        for i in QandA:
            print(i,end=" ")
        print()
    conn.close()

# 영화 데이터 테이블 생성
def create_movie_table():
    conn = sqlite3.connect('portfolio/static/sqlite3/Movie.db')
    cursor=conn.cursor()
    cursor.execute('''CREATE TABLE if not exists Movies(
        num int,
        score int,
        title text,
        opinion text,
        author text,
        date text
    )''')
    conn.commit()
    conn.close()

# 영화 데이터 입력 함수
def insert_movies(trans_data):
    conn = sqlite3.connect('portfolio/static/sqlite3/Movie.db')
    cursor = conn.cursor()
    
    # case 1
    #cursor.execute("INSERT INTO books VALUES('Java','2019-05-20','길벗',500,10)")

    # case 2
    sql = 'INSERT INTO Movies VALUES(?,?,?,?,?,?)'
    #cursor.execute(sql,('Python','201001','한빛',584,20))

    # case 3
    cursor.execute(sql,trans_data)
    conn.commit()
    conn.close()

# 전체 영화 데이터 출력 함수
def all_cine():
    conn=sqlite3.connect('portfolio/static/sqlite3/Movie.db')
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Movies")
    print('[1] 전체 데이터 출력하기')
    Movies=cursor.fetchall()
    print(type(Movies)) # 타입 출력
    print(len(Movies)) # 레코드 개수 출력

    for Movie in Movies:
        for i in Movie:
            print(i,end=" ")
        print()
    conn.close()

def delete_cine():
    conn=sqlite3.connect('portfolio/static/sqlite3/Movie.db')
    cusor=conn.cursor()
    cusor.execute("DELETE FROM Movies")
    conn.commit()
    conn.close()
    print("성공")
