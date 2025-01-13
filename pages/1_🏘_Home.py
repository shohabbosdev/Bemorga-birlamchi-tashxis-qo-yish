import sqlite3
import streamlit as st
import pandas as pd
from io import BytesIO

# Streamlit sahifa sozlamalari
st.set_page_config(page_title="Erta tashxislashning ekspert tizimi", page_icon="💊", layout="wide", initial_sidebar_state="expanded")

# SQLite ma'lumotlar bazasiga ulanish (maxsus timeout bilan)
def get_connection():
    return sqlite3.connect('data/diagnosis_data.db', timeout=10)

# Jadvalni yaratish
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS diseases (
                        id INTEGER PRIMARY KEY, 
                        name TEXT UNIQUE)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS symptom_groups (
                        id INTEGER PRIMARY KEY, 
                        disease_id INTEGER, 
                        group_name TEXT, 
                        FOREIGN KEY(disease_id) REFERENCES diseases(id),
                        UNIQUE(disease_id, group_name))''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS symptoms (
                        id INTEGER PRIMARY KEY, 
                        group_id INTEGER, 
                        symptom_name TEXT, 
                        FOREIGN KEY(group_id) REFERENCES symptom_groups(id))''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS disease_symptoms (
                        id INTEGER PRIMARY KEY, 
                        disease_id INTEGER, 
                        symptom_id INTEGER, 
                        value INTEGER,
                        FOREIGN KEY(disease_id) REFERENCES diseases(id),
                        FOREIGN KEY(symptom_id) REFERENCES symptoms(id),
                        UNIQUE(disease_id, symptom_id))''')
    
    conn.commit()
    conn.close()

# Jadval yaratish funksiyasini ishga tushirish
create_tables()

# Kasalliklarni va simptomlarni o'qish
def get_diseases():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM diseases")
    diseases = cursor.fetchall()
    conn.close()
    return diseases

def get_symptom_groups(disease_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, group_name FROM symptom_groups WHERE disease_id=?", (disease_id,))
    groups = cursor.fetchall()
    conn.close()
    return groups

def get_symptoms(group_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, symptom_name FROM symptoms WHERE group_id=?", (group_id,))
    symptoms = cursor.fetchall()
    conn.close()
    return symptoms


st.markdown("# 💉:rainbow[Kasalliklar bilan ishlash oynasi]")

tabs = st.tabs(["Ma'lumotlarni kiritish", "Ma'lumotlarni tahrirlash", "Excelga eksport qilish"])

with tabs[0]:
    st.subheader("Kasalliklar va Simptomlarni kiritish")
    
    kasalliklar_soni = st.number_input("Nechta kasallik nomini kiritasiz?", 1, 10, 1)
    kasalliklar_nomlari = [st.text_input(f"{i+1}-Kasallik nomini kiriting", key=f'kasallik_{i}') for i in range(kasalliklar_soni)]

    # Kasalliklar uchun simptomlar guruhi va simptomlarni kiritish
    symptom_groups = []
    symptoms = {}

    for i, kasallik in enumerate(kasalliklar_nomlari):
        if kasallik:
            st.markdown(f"### {kasallik} uchun simptomlar guruhi kiritish")
            num_groups = st.number_input(f"{kasallik} uchun simptomlar guruhi sonini kiriting", 0, 5, 1, key=f"num_groups_{i}")
            groups = []
            for j in range(num_groups):
                group_name = st.text_input(f"{j+1}-Simptomlar guruhi nomini kiriting", key=f"group_{i}_{j}")
                if group_name:
                    groups.append(group_name)
                    symptoms[group_name] = st.text_area(f"{group_name} uchun simptomlarni kiriting (vergul bilan ajrating)", key=f"symptoms_{i}_{j}")
            symptom_groups.append((kasallik, groups))

    # Simptomlarga mos ravishda 0 yoki 1 raqamlarini kiritish
    symptom_matrix = []

    for kasallik, groups in symptom_groups:
        for group in groups:
            symptoms_text = symptoms[group]
            symptom_list = [symptom.strip() for symptom in symptoms_text.split(',')]
            
            # Har bir simptom uchun checkbox (0 yoki 1)
            for symptom in symptom_list:
                if symptom:
                    value = st.checkbox(f"Kasallik: {kasallik} | Guruh: {group} | Simptom: {symptom} mavjudmi?", key=f"value_{kasallik}_{group}_{symptom}")
                    symptom_matrix.append([kasallik, group, symptom, 1 if value else 0])

    # Saqlash tugmasi
    saqlash = st.button("Saqlash", disabled=not kasalliklar_nomlari)

    if saqlash:
        st.write(f"Saqlash muvaffaqiyatli bajarildi. Jami {len(kasalliklar_nomlari)} ta kasallik kiritildi.")
        
        # Kasalliklarni va simptomlarni saqlash
        conn = get_connection()
        cursor = conn.cursor()
        
        for kasallik in kasalliklar_nomlari:
            if kasallik:
                # Kasallik nomi bazada mavjudligini tekshirish
                cursor.execute("SELECT id FROM diseases WHERE name=?", (kasallik,))
                disease_id = cursor.fetchone()
                
                if not disease_id:
                    cursor.execute("INSERT INTO diseases (name) VALUES (?)", (kasallik,))
                    disease_id = cursor.lastrowid
                else:
                    disease_id = disease_id[0]

                # Har bir kasallik uchun simptomlar guruhi saqlash
                for group in symptoms:
                    # Simptomlar guruhi bazada mavjudligini tekshirish
                    cursor.execute("SELECT id FROM symptom_groups WHERE disease_id=? AND group_name=?", (disease_id, group))
                    group_id = cursor.fetchone()
                    
                    if not group_id:
                        cursor.execute("INSERT INTO symptom_groups (disease_id, group_name) VALUES (?, ?)", (disease_id, group))
                        group_id = cursor.lastrowid
                    else:
                        group_id = group_id[0]

                        # Har bir simptomni saqlash
                        for symptom in symptoms[group].split(','):
                            symptom = symptom.strip()
                            if symptom:
                                cursor.execute("INSERT INTO symptoms (group_id, symptom_name) VALUES (?, ?)", (group_id, symptom))

                # Simptomlar jadvaliga 0 yoki 1 qiymatlarni saqlash
                data_to_insert = []
                for kasallik, group, symptom, value in symptom_matrix:
                    disease_id = cursor.execute("SELECT id FROM diseases WHERE name=?", (kasallik,)).fetchone()
                    if disease_id:
                        disease_id = disease_id[0]
                        group_id = cursor.execute("SELECT id FROM symptom_groups WHERE disease_id=? AND group_name=?", (disease_id, group)).fetchone()
                        
                        if group_id:
                            group_id = group_id[0]
                            symptom_id = cursor.execute("SELECT id FROM symptoms WHERE group_id=? AND symptom_name=?", (group_id, symptom)).fetchone()
                            
                            if symptom_id:
                                symptom_id = symptom_id[0]
                                
                                # Ma'lumotlar bazasida mavjudligini tekshirish va saqlash
                                cursor.execute("""
                                    INSERT OR IGNORE INTO disease_symptoms (disease_id, symptom_id, value) 
                                    VALUES (?, ?, ?)
                                """, (disease_id, symptom_id, value))

        conn.commit()  # O'zgarishlarni saqlash
        conn.close()  # Ulanishni yopish
        st.success("Ma'lumotlar muvaffaqiyatli saqlandi!")

with tabs[1]:
    st.subheader("Mavjud kasalliklar va simptomlarni tahrirlash yoki o'chirish")

    diseases = get_diseases()
    kasallik_nomlari = [disease[1] for disease in diseases]
    selected_disease = st.selectbox("Kasallikni tanlang", kasallik_nomlari)

    if selected_disease:
        # Kasallikni tahrirlash
        new_name = st.text_input(f"{selected_disease} nomini tahrirlash", value=selected_disease)
        if st.button(f"{selected_disease} nomini yangilash"):
            if new_name:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE diseases SET name=? WHERE name=?", (new_name, selected_disease))
                conn.commit()
                conn.close()
                st.success(f"Kasallik nomi {selected_disease} yangilandi!")

        # Kasallikni o'chirish
        if st.button(f"{selected_disease} kasalligini o'chirish"):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM disease_symptoms WHERE disease_id IN (SELECT id FROM diseases WHERE name=?)", (selected_disease,))
            cursor.execute("DELETE FROM symptom_groups WHERE disease_id IN (SELECT id FROM diseases WHERE name=?)", (selected_disease,))
            cursor.execute("DELETE FROM symptoms WHERE group_id IN (SELECT id FROM symptom_groups WHERE disease_id IN (SELECT id FROM diseases WHERE name=?))", (selected_disease,))
            cursor.execute("DELETE FROM diseases WHERE name=?", (selected_disease,))
            conn.commit()
            conn.close()
            st.success(f"{selected_disease} kasalligi muvaffaqiyatli o'chirildi!")

with tabs[2]:
    st.subheader("Excelga eksport qilish")

    # Faylni eksport qilish
    export_to_excel = st.button("Excelga eksport qilish")

    if export_to_excel:
        # Ma'lumotlarni jadvalga yig'ish
        data = []
        for kasallik, group, symptom, value in symptom_matrix:
            data.append([kasallik, group, symptom, value])
        
        # DataFrame yaratish
        df = pd.DataFrame(data, columns=["Kasallik", "Simptomlar Guruhi", "Simptom", "Qiymat (0 yoki 1)"])
        
        # Faylga saqlash
        file_name = "kasalliklar_va_simptomlar.xlsx"
        
        # BytesIO obyektiga yozish
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Kasalliklar va Simptomlar")
        
        # Foydalanuvchiga faylni yuklab olish imkoniyatini yaratish
        st.download_button(
            label="Excel faylini yuklab olish",
            data=output.getvalue(),
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
