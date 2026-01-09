import mysql.connector

# MySQL 데이터베이스 연결
connection = mysql.connector.connect(
    host="scania.mysql.database.azure.com",       # MySQL 서버 주소
    user="jwkim628",   # 사용자 이름
    password="dnr**2001", # 비밀번호
    database="classicmodels"  # 데이터베이스 이름
)

try:
    # 커서 생성
    cursor = connection.cursor()

    # SQL 쿼리 실행
    table = 'employees'
    query = "SELECT * FROM " + table
    cursor.execute(query)

    # 결과 가져오기
    rows = cursor.fetchall()

    # 결과 출력
    for row in rows:
        print(row)

finally:
    # 연결 종료
    cursor.close()
    connection.close()
