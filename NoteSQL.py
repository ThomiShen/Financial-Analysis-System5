import pymysql

class NoteSql:
    def __init__(self, host,port, user, password, database):
        self.connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor
        )

    def create_table(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS LoveDB (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    gender VARCHAR(50),
                    age INT,
                    job VARCHAR(255),
                    house VARCHAR(255),
                    car VARCHAR(255),
                    interest VARCHAR(255),
                    location VARCHAR(255),
                    visual_age INT,
                    beauty FLOAT,
                    image  Blob
                )
            """)
            self.connection.commit()

    def insert_data(self, user,password):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO admin (user,password)
                VALUES (%s, %s)
            """, (user,password))
            self.connection.commit()

    # def update_data(self):
    #     with self.connection.cursor() as cursor:
    #         cursor.execute("""
    #             ALTER TABLE LoveDB MODIFY image MEDIUMBLOB;
    #         """)
    #         self.connection.commit()

    def fetch_all(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM admin")
            return cursor.fetchall()

    def close(self):
        self.connection.close()


# if __name__ == "__main__":
#     # 测试代码
#     # db = NoteSql(host='localhost', port=3306,user='root', password='12345678', database='test')
#     # db.insert_data("admin","123456")
#     # a=db.fetch_all()
#     # db.close()
#     # print(a)
