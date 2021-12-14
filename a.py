from numpy.lib.function_base import append
from models import Post, UserReactPost, User
from app import db
import numpy as np

def formatInput():
    posts = db.session.execute('select * from cuisine_posts').all()
    users = db.session.execute('select * from users where is_deleted=false').all()
    userReactPostList = db.session.execute('select * from users_react_cookposts').all()

    posts_np = np.empty(shape=[3])
    for userReactPost in userReactPostList:
        posts_np = np.append(posts_np, [userReactPost['user_id'], userReactPost['cookpost_id'], userReactPost['reaction']], axis=0)

    postsList = []
    for post in posts:
        postsList.append(
            Post(
                post['id'],
                post['title'],
                post['thumbnail'],
                post['ratings'],
                post['content'],
                post['created_at'],
                post['updated_at'],
                post['author'],
                post['angry_vote'],
                post['like_vote'],
                post['yummy_vote']
            )
        )

    usersList = []
    for user in users:
        usersList.append(
            User(
                user['id']
            )
        )

    return posts_np, postsList, usersList

def addToPool(user_id, post_id):
    temp = db.session.execute(f'select * from cook_post_pool where user_id={user_id} and cookpost_id={post_id}')

    if temp is None:
        db.session.execute(f'insert into cook_post_pool(user_id, cookpost_id, showed) values({user_id}, {post_id}, false)')