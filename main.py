from flask import Flask, jsonify, url_for, flash, session
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from db import bookshelf, book,read_rate
from operator import itemgetter
import math
import time

app = Flask(__name__)
app.config[' SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '123456'
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:cjx01069599.@192.168.181.81:3306/book'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:20201003886@182.61.132.41:3306/book'
# 协议：mysql+pymysql
# 用户名：root
# 密码：root
# IP地址：localhost
# 端口：3306
# 数据库名：flaskdb #这里的数据库需要提前建好
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


@app.route('/user', methods=['POST', 'GET'])
def enter11():
    if "keyword" in request.form:
        data = db.session.execute(
            "select * from book where book_name REGEXP '" + request.form["keyword"] + "'").fetchall()
        print(data)
        chapter1 = {}
        for i in data:

            try:
                chapter1[i] = db.session.execute("select chapter_name ,chap_id from book_chapters"
                                                 " where chap_id=(select max(chap_id) from "
                                                 "book_chapters where book_chapters.book_id='" + str(
                    i[0]) + "')").fetchall()

            except:
                chapter1[i] = 'null'

        # print(chapter[i])
        book1 = {
            'book': data,
            'chapter': chapter1
        }
        return render_template('首页.html', context=book1)
    if "username" in session:
        recom = []

        a = db.session.execute("select * from bookshelf where user_id='" + session["username"] + "'").fetchall()
        if len(a) != 0:
            username = session["username"]
            mycf = UserBasedCf()
            mycf.get_dataset()
            mycf.calc_user_sim()
            bookids = mycf.recommend(username)
            for i in bookids:
                temp = db.session.execute(
                    "select book_name,book_id from book where book_id='" + str(i) + "'").fetchall()
                recom.append(temp[0])

    if("username" in session.keys()):
        user=session["username"]
        books12=["book1, book2, book3"]

        if request.method=='POST':
            myform=request.form.to_dict()
            books12=myform.keys()
            bookid=[]
            print(books12)
            for i in books12:
                print(i)
                temp=db.session.execute("select book_id from book where book_name='"+eval(i)[0]+"'").fetchall()
                bookid.append(temp[0][0])

            for i in bookid :
                db.session.execute("delete from bookshelf where book_id='"+str(i)+"' and user_id='"+user+"'")
                db.session.execute(
                    "update book.book set collect_count=(select collect_count from(select collect_count from book.book where book_id='" + str(i) + "')a)-1 where book_id='" + str(i) + "'")
            print("shanchuchenggong")

        books = db.session.execute("select book_id from bookshelf where user_id='"+str(user)+"'").fetchall()
        books1=[]
        for i in books:
            temp=db.session.execute("select * from book where book_id='"+str(i[0])+"'").fetchall()
            books1.append(temp[0])
        chapter1 = {}
        for i in books1:
            try:
                chapter1[i] = db.session.execute("select chapter_name ,chap_id from book_chapters"
                                                 " where chap_id=(select max(chap_id) from "
                                                 "book_chapters where book_chapters.book_id='" + str(
                    i[0]) + "')").fetchall()

            except:
                chapter1[i] = 'null'
        book2 = {
            'book': books1,
            'chapter': chapter1,
            'user':user,
            'recom':recom

        }
        return render_template('shujia.html',context=book2)
    else:
        return redirect('/l')

@app.route('/l', methods=['POST', 'GET'])
def enter():
    if request.method == 'POST':
        if "username" in request.form:
            name = request.form["username"]
            if len(name) == 0:
                flash("用户名为空!")
                return redirect(url_for('enter'))
            pwd = request.form["pwd"]
            if len(pwd) == 0:
                flash("密码为空!")
                return redirect(url_for('enter'))
            try:
                a = db.session.execute("select * from users where id='" + name + "' and password=" + pwd).fetchall()
                if len(a) == 0:
                    flash("用户名或密码错误！")
                else:
                    session["username"] = name
                    return redirect(url_for('home'))
            except:
                flash("用户名或密码错误或为空！")

        if "newname" in request.form:
            name = request.form["newname"]
            pwd = request.form["newpwd"]
            if len(name) == 0:
                flash("用户名为空!")
                return render_template('登录界面.html')
            if len(pwd) == 0:
                flash("密码为空!")
                return render_template('登录界面.html')
            try:
                db.session.execute("insert into users values('" + name + "'," + pwd + ")")
                db.session.commit()
                flash("创建成功")
            except:
                flash("用户名已存在")

    return render_template('登录界面.html')


@app.route('/', methods=['GET', 'post'])
def home():
    book = db.session.execute("select * from book ").fetchall()
    chapter = {}
    recom=[]
    if "username" in session:
        a=db.session.execute("select * from bookshelf where user_id='"+session["username"]+"'").fetchall()
        if len(a)!=0:
            username = session["username"]
            mycf=UserBasedCf()
            mycf.get_dataset()
            mycf.calc_user_sim()
            bookids=mycf.recommend(username)
            for i in bookids:
                temp=db.session.execute("select book_name,book_id from book where book_id='"+str(i)+"'").fetchall()
                recom.append(temp[0])

        print(recom)
    else:
        judge = 0
        username=""
        print("未登录")


    if request.method == 'POST':
        if "keyword" in request.form:
            data = db.session.execute(
                "select * from book where book_name REGEXP '" + request.form["keyword"] + "'").fetchall()
            chapter1 = {}
            for i in data:

                try:
                    chapter1[i] = db.session.execute("select chapter_name ,chap_id from book_chapters"
                                                     " where chap_id=(select max(chap_id) from "
                                                     "book_chapters where book_chapters.book_id='" + str(
                        i[0]) + "')").fetchall()

                except:
                    chapter1[i] = 'null'

            book1 = {
                'book': data,
                'chapter': chapter1,
                'recom':recom
            }
            return render_template('首页.html', context=book1)
    for i in book:
        try:
            chapter[i] = db.session.execute("select chapter_name ,chap_id from book_chapters"
                                            " where chap_id=(select max(chap_id) from "
                                            "book_chapters where book_chapters.book_id='" + str(i[0]) + "')").fetchall()

        except:
            chapter[i] = 'null'
    book1 = {
        'book': book,
        'chapter': chapter,
        'recom':recom

    }
    return render_template('首页.html', context=book1)
@app.route('/c/<string:catename>', methods=['GET', 'post'])
def catepage(catename):
    book = db.session.execute("select * from book where cate_name= '"+catename+"'").fetchall()
    chapter = {}
    recom = []
    if "username" in session:

        a = db.session.execute("select * from bookshelf where user_id='" + session["username"] + "'").fetchall()
        if len(a) != 0:
            username = session["username"]
            mycf = UserBasedCf()
            mycf.get_dataset()
            mycf.calc_user_sim()
            bookids = mycf.recommend(username)
            for i in bookids:
                temp = db.session.execute(
                    "select book_name,book_id from book where book_id='" + str(i) + "'").fetchall()
                recom.append(temp[0])

    if request.method == 'POST':
        if "keyword" in request.form:
            data = db.session.execute(
                "select * from book where book_name REGEXP '" + request.form["keyword"] + "'").fetchall()
            chapter1 = {}
            for i in data:

                try:
                    chapter1[i] = db.session.execute("select chapter_name ,chap_id from book_chapters"
                                                     " where chap_id=(select max(chap_id) from "
                                                     "book_chapters where book_chapters.book_id='" + str(
                        i[0]) + "')").fetchall()

                except:
                    chapter1[i] = 'null'
            book1 = {
                'book': data,
                'chapter': chapter1
            }
            return render_template('dushihtml', context=book1)
    for i in book:
        try:
            chapter[i] = db.session.execute("select chapter_name ,chap_id from book_chapters"
                                            " where chap_id=(select max(chap_id) from "
                                            "book_chapters where book_chapters.book_id='" + str(i[0]) + "')").fetchall()

        except:
            chapter[i] = 'null'

    book1 = {
        'book': book,
        'chapter': chapter,
        'recom':recom

    }
    return render_template('dushi.html', context=book1)



@app.route('/<book_id>/<chapter_id>', methods=['GET', 'POST'])
def book_content(book_id, chapter_id):
    if "username" in session.keys():
        userid=session["username"]
        a=db.session.execute("select * from read_rate where user_id='"+userid+"' and book_id="+str(book_id)).fetchall()
        if len(a)==0:
            record = read_rate(
                book_id=book_id,
                user_id=userid,
                chap_id=chapter_id
            )
            db.session.add(record)

        else:
            a=a[0]
            db.session.execute("insert into book.read_rate VALUES (" + str(a[0]) + ", " + str(a[1]) + ",'" + str(userid) + "'," + str(chapter_id) + ")  ON DUPLICATE KEY UPDATE chap_id = '"+str(chapter_id)+"'")
    book1 = book.query.get(book_id)
    if not book1:
        return jsonify(msg='404 not found'), 404
    cate = book1.cate_name
    bname = book1.book_name
    chapter = db.session.execute(
        "select content ,chapter_name from book_chapters where book_id='" + str(book_id) + "'and chap_id='" + str(
            chapter_id) + "'").fetchall()
    if int(chapter_id) < book1.chapter_num and int(chapter_id) > 1:
        prec = int(chapter_id) - 1
        aftc = int(chapter_id) + 1
    elif int(chapter_id) == 1:

        aftc = int(chapter_id) + 1
        prec = int(chapter_id)
        flash("没有上一章啦")
    else:
        aftc = int(chapter_id)
        prec = int(chapter_id) - 1
        flash("已经到最后一章啦")
    data = {
        'bookid': book_id,
        'cate': cate,
        'bname1': bname,
        'id': chapter_id,
        'chapter': chapter,
        'prec': prec,
        'aftc': aftc
    }
    return render_template('阅读.html', context=data)


@app.route('/<book_id>', methods=['GET', 'POST'])
def book_detail(book_id):
   try:
        book1 = book.query.get(book_id)
        if not book1:
            return jsonify(msg='404 not found'), 404
        recom = []
        last=[['','']]
        if "username" in session:


            a = db.session.execute("select * from bookshelf where user_id='" + session["username"] + "'").fetchall()
            if len(a) != 0:
                username = session["username"]
                mycf = UserBasedCf()
                mycf.get_dataset()
                mycf.calc_user_sim()
                bookids = mycf.recommend(username)
                for i in bookids:
                    temp = db.session.execute(
                        "select book_name,book_id from book where book_id='" + str(i) + "'").fetchall()
                    recom.append(temp[0])


            username = session["username"]
            judge = 1
            chapter = db.session.execute("select chap_id from read_rate where '"+book_id+"'=read_rate.book_id and"
                                         " read_rate.user_id= '" + username + "'").fetchall()
            db.session.commit()
            if not chapter:
                html = ""
                b = ""
            else:
                html = chapter[0][0]
                a = chapter[0][0]
                b = db.session.execute(
                    "select chapter_name,chap_id from book_chapters where chap_id="+str(a)+" and book_id="+str(book_id)).fetchall()
            if b:
                print("存在上次阅读")
                last=b
            else:
                print("bucunz")
                last=[['','']]
        else:
            judge = 0
            username=""
            print("未登录")


        if request.method == 'POST':
            if "开始阅读" in request.form:
                first_chapterid = db.session.execute(
                    "select chap_id from book_chapters where book_chapters.book_id='" + str(
                        book_id) + "'").first()
                return redirect('' + book_id + '/' + str(first_chapterid[0]))
            if "keyword" in request.form:
                data = db.session.execute(
                    "select * from book where book_name REGEXP '" + request.form["keyword"] + "'").fetchall()
                print(data)
                chapter1 = {}
                for i in data:
                    print(i)

                    try:
                        chapter1[i] = db.session.execute("select chapter_name ,chap_id from book_chapters"
                                                         " where chap_id=(select max(chap_id) from "
                                                         "book_chapters where book_chapters.book_id='" + str(
                            i[0]) + "')").fetchall()

                    except:
                        chapter1[i] = 'null'

                # print(chapter[i])
                book1 = {
                    'book': data,
                    'chapter': chapter1
                }
                return render_template('首页.html', context=book1)
            if "加入书架" in request.form:  # 加入书架功能
                if (judge == 1):
                    a = db.session.execute("select * from users where id='" + username + "'").fetchall()
                    b = db.session.execute("select * from bookshelf where user_id='" + username + "'and book_id='" + str(
                        book_id) + "'").fetchall()
                    if len(a) == 0:
                        flash("请登录")
                    elif (len(b) != 0):
                        flash("已加入书架")
                    else:
                        record = bookshelf(
                            book_id=book1.book_id,
                            user_id=username,
                        )
                        db.session.execute(
                            "update book set collect_count=(select collect_count from(select collect_count from book where book_id='" + str(book_id) + "')a)+1 where book_id='" + str(book_id) + "'")
                        db.session.add(record)
                        db.session.commit()
                        flash("已加入书架")
                else:
                    flash("请登录")
        chapterret = db.session.execute(
            "select chapter_name,chap_id from book_chapters where book_chapters.book_id='" + str(book_id) + "'").fetchall()
        print(chapterret)
        img = 'cover/' + str(book_id) + '.jpg'
        data = {
            'id': book1.book_id,
            'title': book1.book_name,
            'intro': book1.intro,
            'author': book1.author_name,
            'cate': book1.cate_name,
            'uptime': book1.update_time,
            'chapter': chapterret,
            'img': img,
            'last':last,
            'recom':recom

        }
        return render_template('书籍阅读简介页--目录页1.html', context=data)
   except:
       return jsonify(msg='there is an error'), 404

class UserBasedCf:
    # 初始化
    def __init__(self, users=10, rec=4):
        # 最相似的10个用户
        self.n_sim_user = users
        # 推荐4本书
        self.n_rec_rbook = rec
        # 将数据集划分为训练集和测试集，这里只划了训练集，如果要划测试集数据要多一点
        self.trainSet = {}
        # 用户相似度矩阵
        self.user_sim_matrix = {}
        self.rbook_count = 0

    # 读取书架数据，建立用户-书籍字典
    def get_dataset(self):
        data = {}
        r_b_data =bookshelf.query.all()
        for book1 in r_b_data:
            if book1.user_id not in data:
                data[book1.user_id] = set()
            data[book1.user_id].add(book1.book_id)
            # my_tmp_dict={"book":book.book_id,"user":book.user_id}
            # data.update(**my_tmp_dict)
        self.trainSet = data.copy()

    def calc_user_sim(self):
        # 构建“书籍-用户”倒排索引，一本书对应所有收藏它的用户
        rbook_user = {}

        for user, rbooks in self.trainSet.items():
            for rbook in rbooks:
                if rbook not in rbook_user.keys():
                    rbook_user[rbook] = set()
                rbook_user[rbook].add(user)

        # 计算书籍的数目
        self.rbook_count = len(rbook_user)

        # 初始化用户之间的相似度矩阵：收藏同一本书的两个用户权重加一，之后计算相似度的时候可以忽略权重为0的用户
        for rbook, users in rbook_user.items():
            for u in users:
                for v in users:
                    if u == v:
                        continue
                    self.user_sim_matrix.setdefault(u, {})
                    self.user_sim_matrix[u].setdefault(v, 0)
                    weight = 1
                    # 根据热门程度加权
                    # weight = 1/math.log2(1+len(users))
                    self.user_sim_matrix[u][v] += weight

        # 计算用户之间的相似度
        for u, related_users in self.user_sim_matrix.items():
            for v, count in related_users.items():
                # 余弦相似度公式
                self.user_sim_matrix[u][v] = count / math.sqrt(len(self.trainSet[u]) * len(self.trainSet[v]))
                # Jaccard公式
                # self.user_sim_matrix[u][v] = count / (len(self.trainSet[u]) + len(self.trainSet[v])-count)

    def recommend(self, user):
        # 和用户相似的前K个用户
        K = self.n_sim_user
        # 推荐书的数目
        N = self.n_rec_rbook
        rank = {}
        watched_rbooks = self.trainSet[user]  # 所查询用户收藏的书

        # v是相似用户, wuv是对应相似用户的相似权重，如果两个用户收藏书籍相似度很高，那么这个用户收藏的书籍加权更高
        for v, wuv in sorted(self.user_sim_matrix[user].items(), key=itemgetter(1), reverse=True)[0:K]:
            for rbook in self.trainSet[v]:
                # 用户已经收藏的书直接略过——是否改成用户已经看过的书略过
                if rbook in watched_rbooks:
                    continue
                rank.setdefault(rbook, 0)
                # 统计K个人里有多少观看权重
                rank[rbook] += wuv
        a=sorted(rank.items(), key=itemgetter(1), reverse=True)[0:N]
        book_ids=[]
        for i in a:
            book_ids.append(i[0])

        return book_ids

    # 保存到数据库——是否需要？还是直接计算返回，考虑到收藏数据在不断变化，推荐用户也可能变化
    # 如果要保存，需要新建一个table

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)  # 127.0.0.1 回路 自己返回自己

