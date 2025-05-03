from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
import datetime

app = Flask(__name__)
CORS(app)

# 数据库初始化
def init_db():
    conn = sqlite3.connect('database/diary.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS diaries
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT,
                  content TEXT,
                  mood TEXT,
                  tags TEXT,
                  image_path TEXT,
                  audio_path TEXT,
                  created_at TIMESTAMP)''')
    conn.commit()
    conn.close()

# 确保数据库目录存在
os.makedirs('database', exist_ok=True)
os.makedirs('static/images', exist_ok=True)
os.makedirs('static/audio', exist_ok=True)
init_db()

@app.route('/api/diaries', methods=['GET'])
def get_diaries():
    conn = sqlite3.connect('database/diary.db')
    c = conn.cursor()
    c.execute('SELECT * FROM diaries ORDER BY created_at DESC')
    diaries = c.fetchall()
    conn.close()
    return jsonify(diaries)

@app.route('/api/diaries', methods=['POST'])
def create_diary():
    data = request.form
    title = data.get('title')
    content = data.get('content')
    mood = data.get('mood')
    tags = data.get('tags')
    created_at = datetime.datetime.now()

    image_path = ''
    audio_path = ''

    if 'image' in request.files:
        image = request.files['image']
        image_path = f"static/images/{image.filename}"
        image.save(image_path)

    if 'audio' in request.files:
        audio = request.files['audio']
        audio_path = f"static/audio/{audio.filename}"
        audio.save(audio_path)

    conn = sqlite3.connect('database/diary.db')
    c = conn.cursor()
    c.execute('INSERT INTO diaries (title, content, mood, tags, image_path, audio_path, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
              (title, content, mood, tags, image_path, audio_path, created_at))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Diary created successfully'})

@app.route('/api/diaries/<int:id>', methods=['GET'])
def get_diary(id):
    conn = sqlite3.connect('database/diary.db')
    c = conn.cursor()
    c.execute('SELECT * FROM diaries WHERE id = ?', (id,))
    diary = c.fetchone()
    conn.close()
    return jsonify(diary)

@app.route('/api/diaries/<int:id>', methods=['PUT'])
def update_diary(id):
    data = request.form
    title = data.get('title')
    content = data.get('content')
    mood = data.get('mood')
    tags = data.get('tags')

    conn = sqlite3.connect('database/diary.db')
    c = conn.cursor()
    c.execute('UPDATE diaries SET title = ?, content = ?, mood = ?, tags = ? WHERE id = ?',
              (title, content, mood, tags, id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Diary updated successfully'})

@app.route('/api/diaries/<int:id>', methods=['DELETE'])
def delete_diary(id):
    conn = sqlite3.connect('database/diary.db')
    c = conn.cursor()
    c.execute('DELETE FROM diaries WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Diary deleted successfully'})

@app.route('/api/search', methods=['GET'])
def search_diaries():
    query = request.args.get('query')
    conn = sqlite3.connect('database/diary.db')
    c = conn.cursor()
    c.execute('SELECT * FROM diaries WHERE title LIKE ? OR content LIKE ? OR tags LIKE ? ORDER BY created_at DESC',
              (f'%{query}%', f'%{query}%', f'%{query}%'))
    diaries = c.fetchall()
    conn.close()
    return jsonify(diaries)

@app.route('/api/demo-data', methods=['POST'])
def add_demo_data():
    demo_diaries = [
        {
            'title': '今天的会议',
            'content': '今天参加了一个重要的项目会议，讨论了新产品的开发计划。',
            'mood': '平静',
            'tags': '工作',
            'created_at': datetime.datetime.now() - datetime.timedelta(days=3)
        },
        {
            'title': '周末郊游',
            'content': '周末和家人一起去了郊外野餐，天气很好，心情非常愉快。',
            'mood': '开心',
            'tags': '生活,家庭',
            'created_at': datetime.datetime.now() - datetime.timedelta(days=1)
        },
        {
            'title': '学习新技能',
            'content': '开始学习Python编程，希望能提升自己的技能。',
            'mood': '焦虑',
            'tags': '学习',
            'created_at': datetime.datetime.now() - datetime.timedelta(days=5)
        }
    ]
    conn = sqlite3.connect('database/diary.db')
    c = conn.cursor()
    for diary in demo_diaries:
        c.execute('INSERT INTO diaries (title, content, mood, tags, image_path, audio_path, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
                  (diary['title'], diary['content'], diary['mood'], diary['tags'], '', '', diary['created_at']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Demo data added successfully'})

@app.route('/api/diaries/bulk-delete', methods=['POST'])
def bulk_delete_diaries():
    data = request.get_json()
    ids = data.get('ids', [])
    if not ids:
        return jsonify({'message': 'No diaries selected for deletion'}), 400
    
    conn = sqlite3.connect('database/diary.db')
    c = conn.cursor()
    placeholders = ','.join('?' for _ in ids)
    c.execute(f'DELETE FROM diaries WHERE id IN ({placeholders})', ids)
    conn.commit()
    conn.close()
    return jsonify({'message': 'Diaries deleted successfully'})

@app.route('/api/diaries/all', methods=['DELETE'])
def delete_all_diaries():
    conn = sqlite3.connect('database/diary.db')
    c = conn.cursor()
    c.execute('DELETE FROM diaries')
    conn.commit()
    conn.close()
    return jsonify({'message': 'All diaries deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
