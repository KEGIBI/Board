import pymysql

def get_db_connection():
    return pymysql.connect(
        host='127.0.0.1',  # XAMPP MySQL의 기본 호스트
        user='root',       # 기본 사용자 이름
        password='',       # XAMPP 기본 비밀번호는 없음
        database='board',  # 데이터베이스 이름
        cursorclass=pymysql.cursors.DictCursor
    )

# 데이터베이스 초기화 (테이블 생성)
def init_db():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS posts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            ''')
        connection.commit()
    finally:
        connection.close()
