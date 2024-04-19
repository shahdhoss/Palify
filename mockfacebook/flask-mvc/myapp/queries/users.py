import sqlite3
con = sqlite3.connect("instance\\MainDB.db")
cursor= con.cursor()
table = '''create table bio (
                user_id VARCHAR(255) primary key,
                bio VARCHAR(255),
                foreign key (user_id) references user(user_id)
            )'''
table2='''create table posts(
                id integer PRIMARY KEY,
                user_id VARCHAR(255),
                post VARCHAR(255),
                foreign key (user_id) references user(user_id)
)'''

cursor.execute(table2)
con.commit()
con.close()