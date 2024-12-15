from flask import Flask, request, render_template, redirect, url_for
from db import get_db_connection, init_db

# Flask 애플리케이션 생성
app = Flask(__name__)

# 게시글 목록 조회
def fetch_posts():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM posts ORDER BY created_at DESC;")
            return cursor.fetchall()
    finally:
        connection.close()

# 메인 페이지 (게시글 목록)
@app.route('/')
def index():
    posts = fetch_posts()
    return render_template('index.html', posts=posts)

# 게시글 작성
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s);", (title, content))
            connection.commit()
        finally:
            connection.close()
        return redirect(url_for('index'))
    return render_template('create.html')

# 게시글 수정
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM posts WHERE id = %s;", (post_id,))
            post = cursor.fetchone()
        if not post:
            return "Post not found", 404

        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            with connection.cursor() as cursor:
                cursor.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s;", (title, content, post_id))
            connection.commit()
            return redirect(url_for('index'))
    finally:
        connection.close()

    return render_template('update.html', post=post)

# 게시글 삭제
@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM posts WHERE id = %s;", (post_id,))
        connection.commit()
    finally:
        connection.close()
    return redirect(url_for('index'))

# 게시글 검색
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    criteria = request.args.get('criteria', 'all')
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM posts WHERE "
            if criteria == 'title':
                sql = "SELECT * FROM posts WHERE title LIKE %s"
                cursor.execute(sql, (f"%{query}%",))
            elif criteria == 'content':
                sql = "SELECT * FROM posts WHERE content LIKE %s"
                cursor.execute(sql, (f"%{query}%",))
            else:
                sql = "SELECT * FROM posts WHERE title LIKE %s OR content LIKE %s"
                cursor.execute(sql, (f"%{query}%", f"%{query}%"))
            posts = cursor.fetchall()
    finally:
        connection.close()
    return render_template('index.html', posts=posts, search_query=query)

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM posts WHERE id = %s;", (post_id,))
            post = cursor.fetchone()
        if not post:
            return "Post not found", 404
    finally:
        connection.close()
    return render_template('post.html', post=post)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
