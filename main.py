from flask import Flask, render_template, abort, request, redirect
import random
import string
import os

app = Flask(__name__)
BASE_IMG_PATH = 'static/images/pic01.jpg'
articles = [
    {
        'id': 1,
        'author': 'Petro Petrovich',
        'vievs': 0,
        'img': BASE_IMG_PATH,
        'title': 'Hello world!',
        'text': 'Hello world weqeqweqweHello world weqeqweqweHello world weqeqweqweHello world weqeqweqweHello world weqeqweqwe'
    },
    {
        'id': 2,
        'author': 'Ivan Ivanovich',
        'title': 'World Hello',
        'img': BASE_IMG_PATH,
        'vievs': 0,
        'text': 'World HelloWorld HelloWorld HelloWorld HelloWorld HelloWorld HelloWorld HelloWorld HelloWorld HelloHelloWorld HelloHelloWorld HelloHelloWorld HelloHelloWorld Hello'
    }
]

users = [
{
                'id': 0,
                'username': 'user',
                'email': 'admin@admin.com',
                'phone': '+380645646465',
                'password': 'password',
                'avatar': 'static/images/default_avatar.jpg'
            }
]
@app.route('/')
def main_page():
    return render_template('index.html', title='ItStep Blog', articles=articles)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/article/<int:id>')
def get_article(id):
    for article in articles:
        if article['id'] == id:
            article['vievs']+=1
            return render_template('generic.html', article=article)
    abort(404)


@app.route('/create/article', methods=['GET', 'POST'])
def create_article():
    """
    Request methods:
        1) GET - Отвечает за получение данных
        2) POST - Отвечает за создание данных
        3) PUT - Отвечает за обновление данных
        4) DELETE - Отвечает за удаление данных
    """
    if request.method == 'GET':
        return render_template('create_article.html')
    elif request.method == 'POST':
        image = request.files['article_image']
        random_name = ''.join([random.choice(string.digits + string.ascii_letters) for x in range(10)])
        img_path = f'static/images/{random_name}.jpg'
        image.save(img_path)
        articles.append({
            'id': len(articles) + 1,
            'author': request.form['article_author'],
            'title': request.form['article_title'],
            'img': img_path,
            'views_count': 0,
            'text': request.form['article_text'],
        })
        return redirect('/')
    else:
        return 'METHOD NOT ALLOWED'



data = """
<div class="content">

    <p>{{ article['text'] }}</p>

</div>
"""

data.find('{{')
args = "article['text']"

@app.route('/update/article/<int:id>', methods=['GET', 'POST'])
def update_article(id):
    if request.method == 'GET':
        for article in articles:
            if article['id'] == id:
                return render_template('update_article.html', article=article)
        abort(404)
    elif request.method == 'POST':
        image = request.files['article_image']
        for article in articles:
            if article['id'] == id:
                article['title'] = request.form['article_title']
                article['author'] = request.form['article_author']
                article['text'] = request.form['article_text']
                if image.filename:
                    random_name = ''.join([random.choice(string.digits + string.ascii_letters) for x in range(10)])
                    img_path = f'static/images/{random_name}.jpg'
                    image.save(img_path)
                else:
                    img_path = BASE_IMG_PATH
                if article['img'] != BASE_IMG_PATH:
                    os.remove(article['img'])

                article['img'] = img_path
                return redirect(f'/article/{article["id"]}')



@app.route('/create/user/', methods=['GET', 'POST'])
def create_user():

    if request.method == 'POST':
        try:
            for user in users:
                    user['name'] = request.form['username']
                    users.append({'id': len(users),'name': request.form['username']})
                    if request.form['email'].find('@') and request.form['email'].find('.') :
                        user['email'] = request.form['email']
                        users.append({'email': request.form['email']})
                    else:
                        abort(401)
                    user['phone'] = request.form['phone']
                    users.append({'phone': request.form['phone']})

                    if request.form['password']==request.form['confirm_password']:
                        user['confirm_password'] = request.form['confirm_password']
                        users.append({'confirm_password': request.form['confirm_password']})
                    else:
                        abort(401)
                    user['password'] = request.form['password']
                    users.append({'password': request.form['password']})
                    if 'avatar' in request.files:
                        image = request.files['avatar']
                        random_name = ''.join([random.choice(string.digits + string.ascii_letters) for x in range(10)])
                        img_path = f'static/images/{random_name}.jpg'
                        image.save(img_path)
                    else:
                        img_path = 'static/images/default_avatar.jpg'
            return redirect('/')
        except Exception as e:
                print(e)
                abort(500)

    elif request.method == 'GET':
        return render_template('user_form.html')

    else:
        return 'METHOD NOT ALLOWED'

# @app.route('/create/user', methods=['GET', 'POST'])
# def create_user():
#     if request.method == 'GET':
#         return render_template('user_form.html')
    # # elif request.method == 'POST':
    # #     try:
    # #         if 'avatar' in request.files:
    # #             image = request.files['avatar']
    # #             random_name = ''.join([random.choice(string.digits + string.ascii_letters) for x in range(10)])
    # #             img_path = f'static/images/{random_name}.jpg'
    # #             image.save(img_path)
    # #         else:
    # #             img_path = 'static/images/default_avatar.jpg'
    # #         users.append({
    # #             'id': len(users),
    # #             'username': request.form['username'],
    # #             'email': request.form['email'],
    # #             'phone': request.form['phone'],
    # #             'password': request.form['password'],
    # #             'avatar': img_path
    # #         })
    # #         return redirect('/')
    # #     except Exception as e:
    # #         print(e)
    # #         abort(500)
    # else:
    #     return 'METHOD NOT ALLOWED'
    #

@app.route('/users', methods=['GET'])
def get_users():
    return render_template('users.html', users=users)


@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    for user in users:
        if user['id'] == id:
            return render_template('user.html', user=user)
    abort(418)


@app.route('/delete/user/<int:id>', methods=['GET'])
def delete_user(id):
    global users
    users = list(filter(lambda x: x['id'] != id, users))
    return 'success'



if __name__ == '__main__':
    app.run(host='localhost', port=5000)
