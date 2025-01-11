import streamlit as st
import sqlite3

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# SQLite database connection
def get_connection(db_name):
    return sqlite3.connect(f'data/{db_name}.db')

# Function to fetch user data
def fetch_users(conn, user_type):
    cursor = conn.execute(f"SELECT id, login, parol FROM {user_type}")
    return cursor.fetchall()

# Main function
def main():
    if st.session_state.authenticated:
        st.switch_page("pages/1_🏘_Home.py")
        return

    conn_doctor = get_connection('doctors')
    conn_admin = get_connection('admins')

    # Get user data
    doctors = fetch_users(conn_doctor, 'DOCTORS')
    admins = fetch_users(conn_admin, 'ADMINS')

    # Create username and password mappings
    patient_passwords = {doctor[1]: doctor[2] for doctor in doctors}
    admin_passwords = {admin[1]: admin[2] for admin in admins}

    # Streamlit layout
    col1, col2, col3 = st.columns([1, 5, 1])
    with col2:
        st.title("💥 LOGIN & REGISTER")

        selected_role = st.selectbox("Tizimdagi rolingiz", ['Doktor', 'Admin'])
        input_login = st.text_input("Loginingizni kiriting")
        input_password = st.text_input("Parolingizni kiriting", type='password', placeholder='********')

        ccol1, ccol2 = st.columns(2)
        login_button = ccol1.button('Kirish', use_container_width=True, type='primary', icon='✏️')
        register_button = ccol2.button("Ro'yxatdan o'tish", use_container_width=True, type='secondary', icon='✍️', disabled=(selected_role == 'Admin'))

        # Login process
        if login_button:
            if selected_role == 'Doktor':
                if input_login in patient_passwords and input_password == patient_passwords[input_login]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = 'doctor'
                    st.success(f"Xush kelibsiz, {input_login}!")
                    st.switch_page("pages/1_🏘_Home.py")
                else:
                    st.error("Loginingiz yoki parolingiz noto'g'ri.")
            elif selected_role == 'Admin':
                if input_login in admin_passwords and input_password == admin_passwords[input_login]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = 'admin'
                    st.success(f"Xush kelibsiz, admin {input_login}!")
                    st.switch_page("pages/1_🏘_Home.py")
                else:
                    st.error("Loginingiz yoki parolingiz noto'g'ri.")
            else:
                st.error(f"{selected_role} mavjud emas. Iltimos, to'g'ri ma'lumotlarni kiriting.")

        # Registration process
        if register_button and selected_role == 'Doktor':
            with st.sidebar:
                with st.form("ro'yxatdan o'tish oynasi"):
                    st.write("Ro'yxatdan o'tish oynasi")
                    login = st.text_input("O'z loginingizni kiriting", key="reg_login")
                    email = st.text_input("O'z emailingizni kiriting", key="reg_email")
                    password = st.text_input("O'z parolingizni kiriting", type='password', key="reg_password")
                    password1 = st.text_input("Parolingizni qaytadan kiriting", type='password', key="reg_password1")

                    submitted = st.form_submit_button("Ro'yxatdan o'tish", disabled=(password != password1))
                    if submitted:
                        try:
                            conn_doctor.execute("INSERT INTO DOCTORS (login, parol) VALUES (?, ?)", (login, password))
                            conn_doctor.commit()
                            st.success("Ro'yxatdan o'tish muvaffaqiyatli amalga oshirildi.")
                        except sqlite3.IntegrityError:
                            st.error("Loginingiz undan oldin olingan bo'lishi mumkin. Iltimos, boshqa loginingizni tanlang.")
                        except Exception as e:
                            st.error(f'Xatolik: {e}')

    # Close database connections
    conn_doctor.close()
    conn_admin.close()

if __name__ == "__main__":
    main()