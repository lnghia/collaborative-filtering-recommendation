import re
from flask import Flask
from flask import Flask
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import date

from NNCF import CF

from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

from numpy.lib.function_base import append
from models.Post import Post
from models.User import User
# from models.UserReactPost import 
import numpy as np

def formatInput():
    posts = db.session.execute('select * from cuisine_posts').all()
    users = db.session.execute('select * from users where is_deleted=false').all()
    userReactPostList = db.session.execute('select * from users_react_cookposts').all()

    posts_np = []
    for userReactPost in userReactPostList:
        posts_np.append([userReactPost['user_id'], userReactPost['cookpost_id'], userReactPost['reaction']])
    posts_np = np.array(posts_np)

    postsList = []
    for post in posts:
        postsList.append(
            post['id']
        )

    usersList = []
    for user in users:
        usersList.append(
            user['id']
        )

    return posts_np, postsList, usersList

def addToPool(user_id, post_id):
    today = date.today()

    temp = db.session.execute(f'select * from cook_post_pool where user_id={user_id} and cook_post_id={post_id}').first()

    if temp is None:
        db.session.execute(f'insert into cook_post_pool (cookposts, users, user_id, cook_post_id, showed, added_date) values ({post_id}, {user_id}, {user_id}, {post_id}, false, \'{today.strftime("%Y-%m-%d %H:%M:%S")}\')')
        db.session.commit()
        
def feedUserPostPools():
    print("recommending ...")
    posts_np, posts, users = formatInput()

    rs = CF(posts_np, k = 10, uuCF = 0)
    rs.fit()

    for post in posts:
        for user in users:
            rs.pred(user, post, normalized = 0)
        result = rs.recommend(post)
        print(f'{post} - {result}')
        for tmp in result:
            addToPool(tmp, post)

@app.route("/")
def hello():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=feedUserPostPools, trigger="interval", seconds=30)
    scheduler.start()
    return '<h1>Hello</h1>'

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='34.124.219.37')