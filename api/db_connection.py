import MySQLdb

def connect_to_db():
    # 데이터베이스 연결 설정
    connection = MySQLdb.connect(
        user="admin",
        passwd="XPk84uzWCsQIuI2bdYrB",
        host="localhost",
        db="healthyreal"
    )


    # 연결 확인
    if connection:
        print("데이터베이스에 성공적으로 연결되었습니다.")

    # 연결 반환
    return connection
