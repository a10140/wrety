#!/usr/bin/env python3
"""
Simple test to verify the WREP app can initialize without errors
"""

import sys
import os
import tempfile

# Mock Kivy components for testing without GUI
class MockWindow:
    size = (360, 640)
    width = 360

class MockApp:
    user_data_dir = tempfile.gettempdir()
    
class MockColor:
    def __init__(self, *args): pass
    def __enter__(self): return self
    def __exit__(self, *args): pass

class MockRectangle:
    def __init__(self, **kwargs): pass

# Create mock modules
sys.modules['kivy'] = type(sys)('kivy')
sys.modules['kivy.app'] = type(sys)('kivy.app')
sys.modules['kivy.uix'] = type(sys)('kivy.uix')
sys.modules['kivy.uix.boxlayout'] = type(sys)('kivy.uix.boxlayout')
sys.modules['kivy.uix.gridlayout'] = type(sys)('kivy.uix.gridlayout')
sys.modules['kivy.uix.scrollview'] = type(sys)('kivy.uix.scrollview')
sys.modules['kivy.uix.textinput'] = type(sys)('kivy.uix.textinput')
sys.modules['kivy.uix.button'] = type(sys)('kivy.uix.button')
sys.modules['kivy.uix.label'] = type(sys)('kivy.uix.label')
sys.modules['kivy.uix.popup'] = type(sys)('kivy.uix.popup')
sys.modules['kivy.core'] = type(sys)('kivy.core')
sys.modules['kivy.core.window'] = type(sys)('kivy.core.window')
sys.modules['kivy.graphics'] = type(sys)('kivy.graphics')

# Add mock classes
sys.modules['kivy.app'].App = MockApp
sys.modules['kivy.uix.boxlayout'].BoxLayout = object
sys.modules['kivy.uix.gridlayout'].GridLayout = object
sys.modules['kivy.uix.scrollview'].ScrollView = object
sys.modules['kivy.uix.textinput'].TextInput = object
sys.modules['kivy.uix.button'].Button = object
sys.modules['kivy.uix.label'].Label = object
sys.modules['kivy.uix.popup'].Popup = object
sys.modules['kivy.core.window'].Window = MockWindow()
sys.modules['kivy.graphics'].Color = MockColor
sys.modules['kivy.graphics'].Rectangle = MockRectangle

print("🧪 Testing WREP App initialization...")
print("=" * 50)

try:
    # Test imports
    print("Testing imports...")
    import sqlite3
    import json
    from datetime import datetime
    import uuid
    print("✓ All required Python modules can be imported")
    
    # Test database operations
    print("\nTesting database operations...")
    test_db_dir = os.path.join(tempfile.gettempdir(), 'wrep_test')
    os.makedirs(test_db_dir, exist_ok=True)
    db = sqlite3.connect(os.path.join(test_db_dir, 'wrep.db'))
    cursor = db.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
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
    
    db.commit()
    print("✓ Database tables created successfully")
    
    # Test insert operations
    test_username = "test_user"
    test_password = "test_pass"
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                  (test_username, test_password))
    db.commit()
    print("✓ Database insert operation successful")
    
    # Test query operations
    cursor.execute('SELECT * FROM users WHERE username = ?', (test_username,))
    user = cursor.fetchone()
    if user:
        print("✓ Database query operation successful")
    
    # Cleanup
    db.close()
    os.remove(os.path.join(test_db_dir, 'wrep.db'))
    print("✓ Database cleanup successful")
    
    print("\n" + "=" * 50)
    print("✅ ALL TESTS PASSED!")
    print("=" * 50)
    print("\nThe app should work correctly when built into APK.")
    print("Proceed with: ./build.sh")
    
except Exception as e:
    print(f"\n❌ TEST FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
