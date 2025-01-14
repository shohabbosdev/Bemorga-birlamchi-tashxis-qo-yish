import streamlit as st
import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime, timedelta

# Logging konfiguratsiyasi
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log'
)
logger = logging.getLogger(__name__)

# Constants
DATABASE_DIR = Path('data')
MAX_LOGIN_ATTEMPTS = 3
LOGIN_TIMEOUT_MINUTES = 15

USER_TYPES = {
    'Doktor': {'db_name': 'doctors', 'table': 'DOCTORS'},
    'Administrator': {'db_name': 'admins', 'table': 'ADMINS'}
}

class DatabaseManager:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self.conn
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

class SessionManager:
    @staticmethod
    def create_session(user_data: Dict):
        st.session_state.authenticated = True
        st.session_state.user_role = user_data['role']
        st.session_state.user_id = user_data['id']
        st.session_state.login_time = datetime.now()
        st.session_state.last_activity = datetime.now()
    
    @staticmethod
    def validate_session() -> bool:
        if not st.session_state.get('authenticated'):
            return False
        
        # Session timeout tekshiruvi (30 daqiqa)
        if datetime.now() - st.session_state.last_activity > timedelta(minutes=30):
            SessionManager.end_session()
            return False
        
        st.session_state.last_activity = datetime.now()
        return True
    
    @staticmethod
    def end_session():
        keys = ['authenticated', 'user_role', 'user_id', 'login_time', 'last_activity']
        for key in keys:
            if key in st.session_state:
                del st.session_state[key]

class AuthenticationManager:
    def __init__(self):
        self.attempts = {}
        self.blocked_until = {}
    
    def can_attempt(self, username: str) -> bool:
        now = datetime.now()
        if username in self.blocked_until:
            if now < self.blocked_until[username]:
                return False
            else:
                del self.blocked_until[username]
                if username in self.attempts:
                    del self.attempts[username]
        return True
    
    def record_attempt(self, username: str):
        now = datetime.now()
        if username not in self.attempts:
            self.attempts[username] = 1
        else:
            self.attempts[username] += 1
            
        if self.attempts[username] >= MAX_LOGIN_ATTEMPTS:
            self.blocked_until[username] = now + timedelta(minutes=LOGIN_TIMEOUT_MINUTES)
    
    def authenticate_user(self, login: str, password: str, role: str) -> Optional[Dict]:
        if not self.can_attempt(login):
            st.error(f"Ko'p marta noto'g'ri urinish. {LOGIN_TIMEOUT_MINUTES} daqiqa kutishingiz kerak.")
            return None
        
        user_type = USER_TYPES[role]
        db_path = DATABASE_DIR / f"{user_type['db_name']}.db"
        
        try:
            with DatabaseManager(db_path) as conn:
                cursor = conn.execute(
                    f"SELECT id, login, parol FROM {user_type['table']} WHERE login = ? AND parol = ?",
                    (login, password)
                )
                user = cursor.fetchone()
                
                if user:
                    return {'id': user[0], 'login': user[1], 'role': role}
                
                self.record_attempt(login)
                return None
                
        except sqlite3.Error as e:
            logger.error(f"Autentifikatsiya paytida ma'lumotlar bazasida xatolik yuz berdi: {e}")
            return None


def main():
    # Initialize database directory
    DATABASE_DIR.mkdir(exist_ok=True)
    
    # Check existing session
    if SessionManager.validate_session():
        st.switch_page("pages/1_🏘_Home.py")
        return

    auth_manager = AuthenticationManager()
    # Show UI
    
    st.title("💥 Kirish & Ro'yxatdan o'tish")
    selected_role = st.selectbox("Tizimdagi rolingiz", list(USER_TYPES.keys()))
    input_login = st.text_input("Loginingizni kiriting")
    input_password = st.text_input("Parolingizni kiriting", type='password')

    ccol1, ccol2 = st.columns(2)
    login_button = ccol1.button('Kirish', use_container_width=True, type='primary')
    register_button = ccol2.button("Ro'yxatdan o'tish", use_container_width=True, 
                                    type='secondary', disabled=(selected_role == 'Administrator'))

    if login_button and input_login and input_password:
        user_data = auth_manager.authenticate_user(input_login, input_password, selected_role)
        if user_data:
            SessionManager.create_session(user_data)
            st.success(f"Xush kelibsiz, {user_data['login']}!")
            st.switch_page("pages/1_🏘_Home.py")
        else:
            st.error("Login yoki parol noto'g'ri")

    if register_button and selected_role == 'Doktor':
        register()
@st.dialog("®️o'yxatdan o'tish", width='large')
def register():
    with st.form("registration_form"):
            reg_login = st.text_input("Login")
            reg_password = st.text_input("Parol", type="password")
            reg_password_confirm = st.text_input("Parolni tasdiqlang", type="password")

            submitted = st.form_submit_button("Ro'yxatdan o'tish", use_container_width=True, type='primary', icon='®️')

            if submitted:
                if not reg_login or not reg_password:
                    st.error("Barcha maydonlarni to'ldiring")
                    return
                    
                if reg_password != reg_password_confirm:
                    st.error("Parollar mos kelmadi")
                    return
                
                try:
                    with DatabaseManager(DATABASE_DIR / 'doctors.db') as conn:
                        conn.execute(
                            "INSERT INTO DOCTORS (login, parol) VALUES (?, ?)",
                            (reg_login, reg_password)
                        )
                        conn.commit()
                        st.success("Ro'yxatdan o'tish muvaffaqiyatli amalga oshirildi!")
                except sqlite3.IntegrityError:
                    st.error("Bunday login mavjud")
                except Exception as e:
                    logger.error(f"Registratsiya xatoligi: {e}")
                    st.error("Ro'yxatdan o'tishda xatolik yuz berdi")

if __name__ == "__main__":
    main()