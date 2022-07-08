import os
from flask import Flask, render_template, Response, request, session, jsonify, abort, redirect
from werkzeug.utils import secure_filename

from src.bianhuajiance import BHJC
from src.diwufenlei import DWFL
from src.mubiaojiance import MBJC
from src.mubiaotiqu import MBTQ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///testdb.db")
from sqlalchemy import Column, SmallInteger, Text,Integer,String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Employee(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True,autoincrement=True)
    username = Column(String(255))
    password = Column(String(255))
    telphone = Column(String(11))

metadata.create_all(engine)

Connection = sessionmaker(bind=engine)

# 每次执行数据库操作时，都需要创建一个Connection
con = Connection()

app = Flask(__name__)
UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# useless key, in order to use session
app.secret_key = "super secret key"


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/login&register.html', methods=['GET', 'POST'])
def login_html():
    return render_template('login&register.html')


@app.route('/login', methods=['GET', 'POST'])
def longin():
    data = request.form.to_dict()
    print(data)
    username = data['User']
    password = data['pwd']
    user = con.query(Employee).filter(Employee.username == username).filter(Employee.password == password).first()
    if user:
        return redirect('/function1.html')
    return 'nook'

@app.route('/register', methods=['GET', 'POST'])
def registeer():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        username = data['username']
        password = data['password']
        telphone = data['telphone']
        user = con.query(Employee).filter(Employee.username == username).first()
        if user:
            return redirect('/register')
        obj1 = Employee(username=username,password=password,telphone=telphone)
        con.add(obj1)
        # 提交事务
        con.commit()

        # 关闭session，其实是将连接放回连接池
        con.close()
        return redirect("/login&register.html")


@app.route('/function1.html', methods=['GET', 'POST'])
def fun1():
    print(first_pic,1)
    print(scend_pic,1)
    return render_template('function1.html', first_pic=first_pic,scend_pic=scend_pic)


@app.route('/function2.html', methods=['GET', 'POST'])
def fun2():
    return render_template('function2.html')


@app.route('/function3.html', methods=['GET', 'POST'])
def fun3():
    return render_template('function3.html')


@app.route('/function4.html', methods=['GET', 'POST'])
def fun4():
    return render_template('function4.html')


global first_pic, scend_pic
first_pic = ""
scend_pic = ""

@app.route('/basketball_detection', methods=['GET', 'POST'])
def upload_image():
    global first_pic,scend_pic
    if request.method == 'POST':
        try:
            response = []
            print(request.files)
            f = request.files['avatar']
            # create a secure filename
            filename = secure_filename(f.filename)
            print("filename", filename)
            # save file to /static/uploads
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print("filepath", filepath)
            f.save(filepath)
            first_pic = filepath

            f = request.files['avatar1']
            # create a secure filename
            filename = secure_filename(f.filename)
            print("filename", filename)
            # save file to /static/uploads
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print("filepath", filepath)
            f.save(filepath)
            scend_pic = filepath
        except:
            pass
        return redirect("/function1.html")


@app.route('/mubiaojiance')
def mubiaojiance():
    global first_pic
    res = MBJC(first_pic)
    return jsonify({"img": res})

@app.route('/mubiaotiqu')
def mubiaotiqu():
    global first_pic
    res = MBTQ(first_pic)
    return jsonify({"img": res})

@app.route('/bianhuajiance')
def bianhuajiance():
    global first_pic, scend_pic
    res = BHJC(first_pic,scend_pic)
    return jsonify({"img": res})

@app.route('/diwufenlei')
def diwufenlei():
    global first_pic
    res = DWFL(first_pic)
    return jsonify({"img": res})
#
# @app.route('/sample_analysis', methods=['GET', 'POST'])
# def upload_video():
#     global shooting_result
#     shooting_result['attempts'] = 0
#     shooting_result['made'] = 0
#     shooting_result['miss'] = 0
#     if (os.path.exists("./static/detections/trajectory_fitting.jpg")):
#         os.remove("./static/detections/trajectory_fitting.jpg")
#     if request.method == 'POST':
#         filename = "sample_video.mp4"
#         print("filename", filename)
#         filepath = "./static/uploads/sample_video.mp4"
#         print("filepath", filepath)
#         session['video_path'] = filepath
#         return render_template("shooting_analysis.html")
#
#
# @app.route('/shooting_analysis', methods=['GET', 'POST'])
# def upload_sample_video():
#     global shooting_result
#     shooting_result['attempts'] = 0
#     shooting_result['made'] = 0
#     shooting_result['miss'] = 0
#     if (os.path.exists("./static/detections/trajectory_fitting.jpg")):
#         os.remove("./static/detections/trajectory_fitting.jpg")
#     if request.method == 'POST':
#         f = request.files['video']
#         # create a secure filename
#         filename = secure_filename(f.filename)
#         print("filename", filename)
#         # save file to /static/uploads
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         print("filepath", filepath)
#         f.save(filepath)
#         session['video_path'] = filepath
#         return render_template("shooting_analysis.html")
#
#
# @app.route('/video_feed')
# def video_feed():
#     video_path = session.get('video_path', None)
#     stream = getVideoStream(video_path)
#     return Response(stream,
#                     mimetype='multipart/x-mixed-replace; boundary=frame')
#
#
# @app.route("/result", methods=['GET', 'POST'])
# def result():
#     return render_template("result.html", shooting_result=shooting_result)
#
#
# # disable caching
# @app.after_request
# def after_request(response):
#     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
#     response.headers["Expires"] = 0
#     response.headers["Pragma"] = "no-cache"
#     return response
#
#
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
