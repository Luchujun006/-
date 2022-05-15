from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:20201003886@182.61.132.41:3306/book'
# 协议：mysql+pymysql
# 用户名：root
# 密码：root
# IP地址：localhost
# 端口：3306
# 数据库名：flaskdb #这里的数据库需要提前建好
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
db = SQLAlchemy(app)

# 新建表User
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(64), primary_key=True) #用户名 主码
    password=db.Column(db.String(20))    #密码
    def __repr__(self):
        return '<User %r>' % self.nick_name


class book(db.Model):
    __tablename__ = 'book'  # 表名
    book_id = db.Column(db.Integer, primary_key=True)  # id字段, int 类型,主键
    book_name = db.Column(db.String(300))  # name字段, 字符串类型,唯一
    cate_name=db.Column(db.String(64))                  #分类名称
    author_name=db.Column(db.String(64))                #作者名字
    chapter_num=db.Column(db.Integer)                   #章节总数
    cover=db.Column(db.String(200))                     #书的封面
    intro=db.Column(db.String(2000))                     #书的简介
    word_count=db.Column(db.Integer)                    #书的总字数
    update_time=db.Column(db.String(20))                #书籍更新时间（每周二）
    collect_count=db.Column(db.Integer)                 #收藏数

#新建表bookchapters
class BookChapters(db.Model):
    __tablename__='book_chapters'
    id=db.Column(db.Integer,primary_key=True)    #章表id 主码
    book_id=db.Column(db.Integer, db.ForeignKey('book.book_id'))   #书id 外码
    chap_id = db.Column(db.Integer)  # 章节id
    chapter_name = db.Column(db.String(64))  #章名
    content=db.Column(db.Text(65500))   #内容

#新建表bookshelf
class bookshelf(db.Model):
    __tablename__='bookshelf'
    id=db.Column(db.Integer, primary_key=True)  #书架id 主码
    book_id=db.Column(db.Integer, db.ForeignKey('book.book_id'))   #书id 外码
    user_id = db.Column(db.String(64), db.ForeignKey('users.id'))  # 用户id 外码

class browse_history(db.Model):
    __tablename__='browse_history'
    id = db.Column(db.Integer, primary_key=True)  # 浏览记录id 主码
    book_id=db.Column(db.Integer, db.ForeignKey('book.book_id'))   #书id 外码
    user_id = db.Column(db.String(64), db.ForeignKey('users.id'))  # 用户id 外码

class read_rate(db.Model):
    __tablename__='read_rate'
    id = db.Column(db.Integer, primary_key=True)  # 阅读进度id 主码
    book_id=db.Column(db.Integer, db.ForeignKey('book.book_id'))   #书id 外码
    user_id = db.Column(db.String(64), db.ForeignKey('users.id'))  # 用户id 外码
    chap_id = db.Column(db.Integer)      # 章节id


class Foreign_keys(db.Model):
    __tablename__ = 'foreign_keys'
    id = db.Column(db.Integer, primary_key=True)  # 搜索id 主码
    key_word=db.Column(db.String(64))   #搜索关键词


if __name__ == '__main__':

    db.session.commit()
    app.run(debug=True)
