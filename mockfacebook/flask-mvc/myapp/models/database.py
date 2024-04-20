import sqlite3
from flask_login import UserMixin
class database_base_model:
    def __init__(self, database_name):
        self.database_name = database_name
    def l_tuple_to_list(self,tuplee):                       
        listt =[]
        for item in tuplee:
            for itemm in item:
                listt.append(itemm)        
        return listt    
    def establish_connection(self):
        self.connection = sqlite3.connect(self.database_name, check_same_thread=False)
    def cursor(self):
        return self.connection.cursor()
    def close(self):
        return self.connection.close()
    def commit(self):
        return self.connection.commit()
    def fetch_all(self, table_name):
        data = self.cursor().execute(f'select * from {table_name}')
        return data.fetchall()
    
class user(database_base_model): 
    def __init__(self, database_name):
        super().__init__(database_name)
        self.establish_connection()
    def get_info(self, id):
        cursor=self.cursor().execute("select first_name, last_name from user where id =? ", (id,))
        result=self.l_tuple_to_list(cursor.fetchall())
        return result
    def addpost(self,user_id,post):
        if post!="" and post!=None:
            self.cursor().execute("insert into posts (user_id,post) values(?,?)",(user_id,post))
            self.commit()
    def bio_exists(self, user_id):
        cursor=self.cursor().execute("select count(*) from bio where user_id =?",(user_id,))
        count=cursor.fetchone()[0]
        return count 
    def addbio(self, user_id, bio):
        self.cursor().execute("insert into bio (user_id,bio) values(?,?)",(user_id,bio))
        self.commit()
    def getbio(self, user_id):
        if self.bio_exists(user_id)!=0:
            cursor=self.cursor().execute("select bio from bio where user_id =?",(user_id,))
            bio=cursor.fetchone()[0]
            return bio
        else:
            return None
    def editbio(self, user_id, bio):
        if self.bio_exists(user_id)!=0:
            curr_bio=bio
            prev_bio=self.getbio(user_id)
            if prev_bio is None:
                self.cursor().execute("UPDATE bio SET bio = ? WHERE bio IS NULL", (curr_bio,))
                self.commit()
            else:
                self.cursor().execute("UPDATE bio SET bio = ? WHERE bio = ?", (curr_bio, prev_bio))
                self.commit()
    def posts_exist(self, user_id):
        cursor=self.cursor().execute("select count(*) from posts where user_id =?",(user_id,))
        count=cursor.fetchone()[0]
        return count
    def getposts(self, user_id):
        count=self.posts_exist(user_id)
        if self.posts_exist(user_id)!=0:
            cursor=self.cursor().execute("select post from posts where user_id=?",(user_id,))
            posts=cursor.fetchall()
            posts_list=self.l_tuple_to_list(posts)
            return [posts_list,count]
        else:
            return None
    def list_of_users(self):
        users=self.cursor().execute("select first_name, last_name from User")
        countt=self.cursor().execute("select count(*) from User")
        count=countt.fetchone()[0]
        userss=[users.fetchall()]
        list_of_users=[]
        users=[]
        for i in range(count):
            list_of_users.append([*userss[0][i]])
        for i in list_of_users:
            myuser=", ".join(i)
            myuser=myuser.replace(",","")
            users.append(myuser)
        return users
    def search(self):
        mylist=[]
        for name in self.list_of_users():
            mylist.append(name)
        return mylist
    
# myuser=user("instance\\MainDB.db")
# users=myuser.search()
# print(users)
    
