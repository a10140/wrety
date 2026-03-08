from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
import sqlite3
import json
from datetime import datetime
import uuid
import os

# 设置窗口大小和初始化
Window.size = (360, 640)

class WREPApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = None
        self.current_session = None
        self.db = None
        self.init_db()
        
    def init_db(self):
        """初始化本地SQLite数据库"""
        # Use app's user data directory for database storage
        try:
            db_path = os.path.join(self.user_data_dir, 'wrep.db')
        except AttributeError:
            db_path = 'wrep.db'
        
        self.db = sqlite3.connect(db_path)
        cursor = self.db.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                display_name TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Add display_name column to existing databases (migration)
        try:
            cursor.execute('ALTER TABLE users ADD COLUMN display_name TEXT DEFAULT ""')
            self.db.commit()
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_sessions (
                session_id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                title TEXT DEFAULT 'New Chat',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES users(username)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES chat_sessions(session_id)
            )
        ''')
        
        self.db.commit()

    def build(self):
        """构建主界面"""
        self.root = BoxLayout(orientation='vertical', size_hint=(1, 1))
        
        # 如果未登录，显示登录界面
        if not self.user:
            self.show_login()
        else:
            self.show_chat()
        
        return self.root

    def show_login(self):
        """显示登录界面"""
        self.root.clear_widgets()
        
        login_layout = BoxLayout(orientation='vertical', padding=20, spacing=15, size_hint=(1, 1))
        
        # 标题
        title = Label(text='WREP AI Console', size_hint_y=0.15, font_size='28sp', bold=True)
        login_layout.add_widget(title)
        
        # 用户名输入
        username_input = TextInput(
            multiline=False, 
            hint_text='Username',
            size_hint_y=0.1,
            padding=10
        )
        login_layout.add_widget(username_input)
        
        # 密码输入
        password_input = TextInput(
            multiline=False,
            hint_text='Password',
            password=True,
            size_hint_y=0.1,
            padding=10
        )
        login_layout.add_widget(password_input)
        
        # 按钮布局
        btn_layout = BoxLayout(size_hint_y=0.15, spacing=10)
        
        def login_action():
            cursor = self.db.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                         (username_input.text, password_input.text))
            user = cursor.fetchone()
            if user:
                self.user = username_input.text
                self.create_new_session()
                self.show_chat()
            else:
                self.show_message('登录失败', '用户名或密码错误')
        
        def register_action():
            cursor = self.db.cursor()
            try:
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                             (username_input.text, password_input.text))
                self.db.commit()
                self.show_message('成功', '注册成功，请重新登录')
                username_input.text = ''
                password_input.text = ''
            except sqlite3.IntegrityError:
                self.show_message('错误', '用户已存在')
        
        login_btn = Button(text='登录', size_hint_x=0.5)
        login_btn.bind(on_press=lambda x: login_action())
        btn_layout.add_widget(login_btn)
        
        register_btn = Button(text='注册', size_hint_x=0.5)
        register_btn.bind(on_press=lambda x: register_action())
        btn_layout.add_widget(register_btn)
        
        login_layout.add_widget(btn_layout)
        
        # 空白区域
        login_layout.add_widget(Label(size_hint_y=0.5))
        
        self.root.add_widget(login_layout)

    def create_new_session(self):
        """创建新的聊天会话"""
        self.current_session = str(uuid.uuid4())
        cursor = self.db.cursor()
        cursor.execute(
            'INSERT INTO chat_sessions (session_id, username, title) VALUES (?, ?, ?)',
            (self.current_session, self.user, 'New Chat')
        )
        self.db.commit()

    def show_chat(self):
        """显示聊天界面"""
        self.root.clear_widgets()
        
        main_layout = BoxLayout(orientation='horizontal', size_hint=(1, 1))
        
        # 侧边栏
        sidebar = BoxLayout(orientation='vertical', size_hint=(0.25, 1), padding=10, spacing=10)
        sidebar.canvas.before.clear()
        with sidebar.canvas.before:
            Color(0.04, 0.04, 0.05, 1)
            Rectangle(size=sidebar.size, pos=sidebar.pos)
        
        # LOGO
        logo = Label(text='WREP', size_hint_y=0.1, font_size='24sp', bold=True)
        sidebar.add_widget(logo)
        
        # 新建聊天按钮
        new_chat_btn = Button(text='+ New Chat', size_hint_y=0.1)
        new_chat_btn.bind(on_press=lambda x: self.new_chat_action())
        sidebar.add_widget(new_chat_btn)
        
        # 历史记录
        history_label = Label(text='History', size_hint_y=0.05, size_hint_min_y=20)
        sidebar.add_widget(history_label)
        
        history_scroll = ScrollView(size_hint=(1, 0.6))
        history_list = GridLayout(cols=1, spacing=5, size_hint_y=None, padding=5)
        history_list.bind(minimum_height=history_list.setter('height'))
        
        cursor = self.db.cursor()
        cursor.execute('SELECT session_id, title FROM chat_sessions WHERE username = ? ORDER BY created_at DESC',
                      (self.user,))
        for row in cursor.fetchall():
            session_id, title = row
            btn = Button(text=title[:20], size_hint_y=None, height=40)
            btn.bind(on_press=lambda x, sid=session_id: self.load_session(sid))
            history_list.add_widget(btn)
        
        history_scroll.add_widget(history_list)
        sidebar.add_widget(history_scroll)
        
        # 个人资料按钮
        profile_btn = Button(text='Profile', size_hint_y=0.1)
        profile_btn.bind(on_press=lambda x: self.show_profile())
        sidebar.add_widget(profile_btn)

        # 退出按钮
        logout_btn = Button(text='Logout', size_hint_y=0.1)
        logout_btn.bind(on_press=lambda x: self.logout())
        sidebar.add_widget(logout_btn)
        
        main_layout.add_widget(sidebar)
        
        # 聊天区域
        chat_layout = BoxLayout(orientation='vertical', size_hint=(0.75, 1), padding=10, spacing=10)
        
        # 聊天消息区
        chat_scroll = ScrollView(size_hint=(1, 0.85))
        self.chat_messages = GridLayout(cols=1, spacing=8, size_hint_y=None, padding=10)
        self.chat_messages.bind(minimum_height=self.chat_messages.setter('height'))
        
        self.load_messages()
        
        chat_scroll.add_widget(self.chat_messages)
        chat_layout.add_widget(chat_scroll)
        
        # 输入区
        input_layout = BoxLayout(size_hint_y=0.15, spacing=5)
        self.input_text = TextInput(multiline=True, hint_text='Type a message...', size_hint_x=0.8)
        send_btn = Button(text='Send', size_hint_x=0.2)
        send_btn.bind(on_press=lambda x: self.send_message())
        input_layout.add_widget(self.input_text)
        input_layout.add_widget(send_btn)
        
        chat_layout.add_widget(input_layout)
        
        main_layout.add_widget(chat_layout)
        self.root.add_widget(main_layout)

    def load_messages(self):
        """加载当前会话的消息"""
        self.chat_messages.clear_widgets()
        if not self.current_session:
            return
        
        cursor = self.db.cursor()
        cursor.execute('SELECT role, content FROM messages WHERE session_id = ? ORDER BY created_at',
                      (self.current_session,))
        
        for role, content in cursor.fetchall():
            msg_label = Label(
                text=f'[{role}]: {content}',
                size_hint_y=None,
                height=80,
                text_size=(self.chat_messages.width - 20, None),
                markup=True
            )
            self.chat_messages.add_widget(msg_label)

    def send_message(self):
        """发送消息"""
        if not self.input_text.text.strip():
            return
        
        cursor = self.db.cursor()
        
        # 保存用户消息
        cursor.execute(
            'INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)',
            (self.current_session, 'user', self.input_text.text)
        )
        self.db.commit()
        
        # 模拟AI响应
        ai_response = "这是一个模拟响应。服务器配置后会有真实的AI回复。"
        cursor.execute(
            'INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)',
            (self.current_session, 'assistant', ai_response)
        )
        self.db.commit()
        
        self.input_text.text = ''
        self.load_messages()

    def load_session(self, session_id):
        """加载指定的会话"""
        self.current_session = session_id
        self.load_messages()

    def new_chat_action(self):
        """创建新聊天"""
        self.create_new_session()
        self.chat_messages.clear_widgets()

    def show_profile(self):
        """显示个人资料编辑界面"""
        cursor = self.db.cursor()
        cursor.execute('SELECT display_name FROM users WHERE username = ?', (self.user,))
        row = cursor.fetchone()
        current_display_name = row[0] if row and row[0] else ''

        popup_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        popup_layout.add_widget(Label(text=f'Username: {self.user}', size_hint_y=0.12))

        popup_layout.add_widget(Label(text='Display Name:', size_hint_y=0.1))
        display_name_input = TextInput(
            multiline=False,
            text=current_display_name,
            hint_text='Display Name (optional)',
            size_hint_y=0.12,
            padding=8
        )
        popup_layout.add_widget(display_name_input)

        popup_layout.add_widget(Label(text='New Password (leave blank to keep current):', size_hint_y=0.1))
        new_password_input = TextInput(
            multiline=False,
            hint_text='New Password',
            password=True,
            size_hint_y=0.12,
            padding=8
        )
        popup_layout.add_widget(new_password_input)

        popup_layout.add_widget(Label(text='Confirm New Password:', size_hint_y=0.1))
        confirm_password_input = TextInput(
            multiline=False,
            hint_text='Confirm New Password',
            password=True,
            size_hint_y=0.12,
            padding=8
        )
        popup_layout.add_widget(confirm_password_input)

        btn_layout = BoxLayout(size_hint_y=0.15, spacing=10)

        popup = Popup(title='Edit Profile', content=popup_layout, size_hint=(0.9, 0.85))

        def save_action():
            self.update_profile(
                display_name_input.text.strip(),
                new_password_input.text,
                confirm_password_input.text,
                popup
            )

        save_btn = Button(text='Save')
        save_btn.bind(on_press=lambda x: save_action())
        btn_layout.add_widget(save_btn)

        cancel_btn = Button(text='Cancel')
        cancel_btn.bind(on_press=popup.dismiss)
        btn_layout.add_widget(cancel_btn)

        popup_layout.add_widget(btn_layout)
        popup.open()

    def update_profile(self, display_name, new_password, confirm_password, popup):
        """保存用户资料更新"""
        if new_password:
            if new_password != confirm_password:
                self.show_message('错误', '两次输入的密码不一致')
                return
            if len(new_password) < 8:
                self.show_message('错误', '密码长度至少为8位')
                return
            cursor = self.db.cursor()
            cursor.execute(
                'UPDATE users SET display_name = ?, password = ? WHERE username = ?',
                (display_name, new_password, self.user)
            )
        else:
            cursor = self.db.cursor()
            cursor.execute(
                'UPDATE users SET display_name = ? WHERE username = ?',
                (display_name, self.user)
            )
        self.db.commit()
        popup.dismiss()
        self.show_message('成功', '个人资料已更新')

    def logout(self):
        """退出登录"""
        self.user = None
        self.current_session = None
        self.show_login()

    def show_message(self, title, message):
        """显示提示消息"""
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_layout.add_widget(Label(text=message))
        
        close_btn = Button(text='OK', size_hint_y=0.3)
        popup_layout.add_widget(close_btn)
        
        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.4))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    WREPApp().run()
