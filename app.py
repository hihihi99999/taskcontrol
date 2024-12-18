import streamlit as st
import sqlite3
from datetime import datetime
import os

# データベースの初期化
def init_db():
    if not os.path.exists('tasks.db'):
        with sqlite3.connect('tasks.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    task_name TEXT NOT NULL,
                    hours REAL NOT NULL,
                    completed BOOLEAN DEFAULT 0
                )
            ''')
            conn.commit()

# タスクの追加
def add_task(date, task_name, hours):
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tasks (date, task_name, hours, completed) VALUES (?, ?, ?, 0)',
            (date, task_name, hours)
        )
        conn.commit()

# タスクの取得
def get_tasks():
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks ORDER BY date DESC')
        return cursor.fetchall()

# タスクの削除
def delete_task(task_id):
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()

# タスクの完了状態を切り替え
def toggle_task(task_id):
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT completed FROM tasks WHERE id = ?', (task_id,))
        current_state = cursor.fetchone()[0]
        new_state = not bool(current_state)
        cursor.execute(
            'UPDATE tasks SET completed = ? WHERE id = ?',
            (int(new_state), task_id)
        )
        conn.commit()

# データベースの初期化
init_db()

# アプリケーションのタイトル
st.title('タスク管理システム')

# 新規タスク登録フォーム
st.header('新規タスク登録')
with st.form('task_form'):
    date = st.date_input('日付')
    task_name = st.text_input('タスク名')
    hours = st.number_input('作業時間（時間）', min_value=0.0, step=0.5)
    submit = st.form_submit_button('登録')
    
    if submit and task_name and hours >= 0:
        add_task(date.strftime('%Y-%m-%d'), task_name, hours)
        st.success('タスクが登録されました')

# タスク一覧の表示
st.header('タスク一覧')
tasks = get_tasks()

if tasks:
    for task in tasks:
        task_id, date, name, hours, completed = task
        col1, col2, col3 = st.columns([1, 8, 1])
        
        with col1:
            if st.checkbox('', value=bool(completed), key=f'check_{task_id}'):
                toggle_task(task_id)
                st.rerun()
        
        with col2:
            status = '(完了)' if completed else ''
            st.write(f'**{date}**: {name} - {hours}時間 {status}')
        
        with col3:
            if st.button('削除', key=f'delete_{task_id}'):
                delete_task(task_id)
                st.rerun()
else:
    st.info('タスクはありません')
