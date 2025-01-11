import json
import streamlit as st

st.set_page_config(page_title="Экспертная система ранней диагностики", page_icon="💊", layout="wide", initial_sidebar_state="expanded")

if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.switch_page("1_💠_Dashboard.py")
    st.stop()
    
# Define Symptom and Illness Classes
class Symptom:
    def __init__(self, name, id_code):
        self.name = name
        self.id_code = id_code

class Illness:
    def __init__(self, name):
        self.name = name
        self.symptoms = {}
    
    def add_symptom(self, symptom, reference):
        self.symptoms[symptom.name] = reference

class Patient:
    def __init__(self, name):
        self.name = name
        self.symptoms = {}
    
    def add_symptom(self, symptom, value):
        self.symptoms[symptom] = value

class Calculation:
    def __init__(self, patient):
        self.patient = patient
        self.illnesses = []
    
    def add_illness(self, illness):
        self.illnesses.append(illness)
    
    def calculate(self):
        results = {}
        for illness in self.illnesses:
            match_count = 0
            for symptom, reference in illness.symptoms.items():
                if symptom in self.patient.symptoms:
                    patient_value = self.patient.symptoms[symptom]
                    if patient_value == reference:
                        match_count += 1
            score = (match_count / len(illness.symptoms)) * 100
            results[illness.name] = score
        return results
import sqlite3
conn = sqlite3.connect('data/userdata.db')

# Load data (familiya, ism, shariflar)
cursor = conn.execute("SELECT id, fish from USERS")


# Extract full names from JSON
patient_names = [row[1] for row in cursor]  

# UI for patient diagnosis
st.title("💥 Экспертная система ранней диагностики")

selected_name = st.selectbox("Выберите пациента", patient_names)
tab1, tab2, tab3, tab4, tab5 = st.tabs(["💥 Экспертная система ранней диагностики", "🥼 Атака артрита", "🧪 Тесты на РФ и АЦЦП","📉 Показательные Анализы", "📄 Переносимые процессы и\или болезни"])

with tab1:
    with st.container(border=True):
        # Patient information (select from JSON file)
        patient = Patient(selected_name)
        # Checkbox inputs for each symptom
        st.subheader("Выберите симптомы пациента")
        symptoms_list = [
            Symptom("1 Крупный сустав (покраснение)", "x1"),
            Symptom("2-10 крупных суставов", "x2"),
            Symptom("1-3 мелких сустава (без учета крупных)", "x3"),
            Symptom("4-10 мелких сустава (без учета крупных)", "x4"),
            Symptom(">10 суставов (как минимум 1 мелкий сустав)", "x5"),
            Symptom("Вовлечение первого плюснефалангового сустава", "x6"),
            Symptom("Энтезопатии (боль в пятке, боль в проекции большеберцового бугра)", "x7"),
            Symptom("Воспалительная боль в нижнем отделе спины: сакроилеит", "x8"),
            Symptom("Воспалительная боль в нижнем отделе спины: спондилит", "x9"),
            Symptom("Воспаление связок и сухожилий в месте их прикрепления к седалищному бугру", "x10"),
        ]

        # Checkbox for each symptom
        for symptom in symptoms_list:
            selected = st.checkbox(symptom.name)
            patient.add_symptom(symptom.name, "+" if selected else "-")

        # Define Illnesses and their reference symptoms
        illness1 = Illness("Ревматоидный артрит")
        illness2 = Illness("Подагрический артрит")
        illness3 = Illness("Реактивный артрит")

        # Add symptoms to the illnesses based on reference answers
        illness1.add_symptom(symptoms_list[0], "-")
        illness1.add_symptom(symptoms_list[1], "+")
        illness1.add_symptom(symptoms_list[2], "+")
        illness1.add_symptom(symptoms_list[3], "+")
        illness1.add_symptom(symptoms_list[4], "+")
        illness1.add_symptom(symptoms_list[5], "-")
        illness1.add_symptom(symptoms_list[6], "-")
        illness1.add_symptom(symptoms_list[7], "-")
        illness1.add_symptom(symptoms_list[8], "-")
        illness1.add_symptom(symptoms_list[9], "-")

        illness2.add_symptom(symptoms_list[0], "+")
        illness2.add_symptom(symptoms_list[1], "-")
        illness2.add_symptom(symptoms_list[2], "-")
        illness2.add_symptom(symptoms_list[3], "-")
        illness2.add_symptom(symptoms_list[4], "-")
        illness2.add_symptom(symptoms_list[5], "+")
        illness2.add_symptom(symptoms_list[6], "-")
        illness2.add_symptom(symptoms_list[7], "-")
        illness2.add_symptom(symptoms_list[8], "-")
        illness2.add_symptom(symptoms_list[9], "-")

        illness3.add_symptom(symptoms_list[0], "-")
        illness3.add_symptom(symptoms_list[1], "-")
        illness3.add_symptom(symptoms_list[2], "-")
        illness3.add_symptom(symptoms_list[3], "-")
        illness3.add_symptom(symptoms_list[4], "-")
        illness3.add_symptom(symptoms_list[5], "-")
        illness3.add_symptom(symptoms_list[6], "+")
        illness3.add_symptom(symptoms_list[7], "+")
        illness3.add_symptom(symptoms_list[8], "+")
        illness3.add_symptom(symptoms_list[9], "+")

        # Perform calculation
        calc = Calculation(patient)
        calc.add_illness(illness1)
        calc.add_illness(illness2)
        calc.add_illness(illness3)
    
with tab2:
    st.header("🥼 Атака артрита")
    with st.container(border=True):
        # Patient information (select from JSON file)
        patient = Patient(selected_name)
        # Checkbox inputs for each symptom
        st.subheader("Выберите симптомы пациента")
        symptoms_list = [
            Symptom("Достижение максимальных проявлений артрита во время атаки за один день", "x1"),
            Symptom("Одна или более атак артрита в анамнезе", "x2"),
            Symptom("Периферический артрит (несимметричный, олигоартрит)", "x3")
        ]

        # Checkbox for each symptom
        for symptom in symptoms_list:
            selected = st.checkbox(symptom.name)
            patient.add_symptom(symptom.name, "+" if selected else "-")

        # Define Illnesses and their reference symptoms
        illness1 = Illness("Ревматоидный артрит")
        illness2 = Illness("Подагрический артрит")
        illness3 = Illness("Реактивный артрит")

        # Add symptoms to the illnesses based on reference answers
        illness1.add_symptom(symptoms_list[0], "+")
        illness1.add_symptom(symptoms_list[1], "+")
        illness1.add_symptom(symptoms_list[2], "-")

        illness2.add_symptom(symptoms_list[0], "+")
        illness2.add_symptom(symptoms_list[1], "+")
        illness2.add_symptom(symptoms_list[2], "-")

        illness3.add_symptom(symptoms_list[0], "-")
        illness3.add_symptom(symptoms_list[1], "-")
        illness3.add_symptom(symptoms_list[2], "+")

        # Perform calculation
        calc = Calculation(patient)
        calc.add_illness(illness1)
        calc.add_illness(illness2)
        calc.add_illness(illness3)
        
with tab3:
    st.header("🧪 Тесты на РФ и АЦЦП")
    with st.container(border=True):
        # Patient information (select from JSON file)
        patient = Patient(selected_name)
        # Checkbox inputs for each symptom
        st.subheader("Выберите симптомы пациента")
        symptoms_list = [
            Symptom("Отрицательны", "x1"),
            Symptom("Слабо позитивны для РФ или АЦЦП (превысили границу нормы, но менее, чем в 3 раза)", "x2"),
            Symptom("Высоко позитивны для РФ или АЦЦП (более, чем в 3 раза превысили границу нормы)", "x3")
        ]

        # Checkbox for each symptom
        for symptom in symptoms_list:
            selected = st.checkbox(symptom.name)
            patient.add_symptom(symptom.name, "+" if selected else "-")

        # Define Illnesses and their reference symptoms
        illness1 = Illness("Ревматоидный артрит")
        illness2 = Illness("Подагрический артрит")
        illness3 = Illness("Реактивный артрит")

        # Add symptoms to the illnesses based on reference answers
        illness1.add_symptom(symptoms_list[0], "-")
        illness1.add_symptom(symptoms_list[1], "+")
        illness1.add_symptom(symptoms_list[2], "+")

        illness2.add_symptom(symptoms_list[0], "-")
        illness2.add_symptom(symptoms_list[1], "-")
        illness2.add_symptom(symptoms_list[2], "-")

        illness3.add_symptom(symptoms_list[0], "-")
        illness3.add_symptom(symptoms_list[1], "-")
        illness3.add_symptom(symptoms_list[2], "-")

        # Perform calculation
        calc = Calculation(patient)
        calc.add_illness(illness1)
        calc.add_illness(illness2)
        calc.add_illness(illness3)

with tab4:
    st.header("📉 Показательные Анализы")
    with st.container(border=True):
        # Patient information (select from JSON file)
        patient = Patient(selected_name)
        # Checkbox inputs for each symptom
        st.subheader("Выберите симптомы пациента")
        symptoms_list = [
            Symptom("Норма по СОЭ ( Скорость оседания эритроцитов) и СРБ (С-реактивный белок)", "x1"),
            Symptom("Повышение СОЭ или уровня СРБ", "x2"),
            Symptom("Мочевая кислота >6,0 мг/дл (360 мкмоль/л)", "x3")
        ]

        # Checkbox for each symptom
        for symptom in symptoms_list:
            selected = st.checkbox(symptom.name)
            patient.add_symptom(symptom.name, "+" if selected else "-")

        # Define Illnesses and their reference symptoms
        illness1 = Illness("Ревматоидный артрит")
        illness2 = Illness("Подагрический артрит")
        illness3 = Illness("Реактивный артрит")

        # Add symptoms to the illnesses based on reference answers
        illness1.add_symptom(symptoms_list[0], "-")
        illness1.add_symptom(symptoms_list[1], "+")
        illness1.add_symptom(symptoms_list[2], "-")

        illness2.add_symptom(symptoms_list[0], "-")
        illness2.add_symptom(symptoms_list[1], "-")
        illness2.add_symptom(symptoms_list[2], "+")

        illness3.add_symptom(symptoms_list[0], "-")
        illness3.add_symptom(symptoms_list[1], "-")
        illness3.add_symptom(symptoms_list[2], "-")

        # Perform calculation
        calc = Calculation(patient)
        calc.add_illness(illness1)
        calc.add_illness(illness2)
        calc.add_illness(illness3)

with tab5:
    st.header("📄 Переносимые процессы и\или болезни")
    with st.container(border=True):
        # Patient information (select from JSON file)
        patient = Patient(selected_name)
        # Checkbox inputs for each symptom
        st.subheader("Выберите симптомы пациента")
        symptoms_list = [
            Symptom("Синовит< 6 нед.", "x1"),
            Symptom("Синовит >=6 нед.", "x2"),
            Symptom("Гипертензия и/или одна или более кардиоваскулярных болезней", "x3"),
            Symptom("Конъюнктивит", "x4"),
            Symptom("Уретрит, простатит", "x5"),
            Symptom("Эндоскопические признаки поражения кишечника", "x6"),
            Symptom("Бленнорагическая кератодермия", "x7"),
            Symptom("Эрозивный круговидный баланит (4–20%)", "x8"),
            Symptom("Язвы слизистой оболочки полости рта", "x9"),
            Symptom("Гиперкератоз ногтей", "x10"),
            Symptom("Нарушения проводимости по данным ЭКГ", "x11"),
            Symptom("Мужской пол", "x12"),
            Symptom("Женский пол", "x13")
        ]

        # Checkbox for each symptom
        for symptom in symptoms_list:
            selected = st.checkbox(symptom.name)
            patient.add_symptom(symptom.name, "+" if selected else "-")

        # Define Illnesses and their reference symptoms
        illness1 = Illness("Ревматоидный артрит")
        illness2 = Illness("Подагрический артрит")
        illness3 = Illness("Реактивный артрит")

        # Add symptoms to the illnesses based on reference answers
        illness1.add_symptom(symptoms_list[0], "-")
        illness1.add_symptom(symptoms_list[1], "+")
        illness1.add_symptom(symptoms_list[2], "-")
        illness1.add_symptom(symptoms_list[3], "-")
        illness1.add_symptom(symptoms_list[4], "-")
        illness1.add_symptom(symptoms_list[5], "-")
        illness1.add_symptom(symptoms_list[6], "-")
        illness1.add_symptom(symptoms_list[7], "-")
        illness1.add_symptom(symptoms_list[8], "-")
        illness1.add_symptom(symptoms_list[9], "-")
        illness1.add_symptom(symptoms_list[10], "-")
        illness1.add_symptom(symptoms_list[11], "-")
        illness1.add_symptom(symptoms_list[12], "-")

        illness2.add_symptom(symptoms_list[0], "-")
        illness2.add_symptom(symptoms_list[1], "-")
        illness2.add_symptom(symptoms_list[2], "+")
        illness2.add_symptom(symptoms_list[3], "-")
        illness2.add_symptom(symptoms_list[4], "-")
        illness2.add_symptom(symptoms_list[5], "-")
        illness2.add_symptom(symptoms_list[6], "-")
        illness2.add_symptom(symptoms_list[7], "-")
        illness2.add_symptom(symptoms_list[8], "-")
        illness2.add_symptom(symptoms_list[9], "-")
        illness2.add_symptom(symptoms_list[10], "-")
        illness2.add_symptom(symptoms_list[11], "-")
        illness2.add_symptom(symptoms_list[12], "-")

        illness3.add_symptom(symptoms_list[0], "-")
        illness3.add_symptom(symptoms_list[1], "-")
        illness3.add_symptom(symptoms_list[2], "-")
        illness3.add_symptom(symptoms_list[3], "+")
        illness3.add_symptom(symptoms_list[4], "+")
        illness3.add_symptom(symptoms_list[5], "+")
        illness3.add_symptom(symptoms_list[6], "+")
        illness3.add_symptom(symptoms_list[7], "+")
        illness3.add_symptom(symptoms_list[8], "+")
        illness3.add_symptom(symptoms_list[9], "+")
        illness3.add_symptom(symptoms_list[10], "+")
        illness3.add_symptom(symptoms_list[11], "-")
        illness3.add_symptom(symptoms_list[12], "-")

        # Perform calculation
        calc = Calculation(patient)
        calc.add_illness(illness1)
        calc.add_illness(illness2)
        calc.add_illness(illness3)


import random
with st.sidebar:
    with st.container(border=True):
        if st.button("Рассчитать результат", icon="🗝"):
            results = calc.calculate()
            st.subheader("Результаты диагностики")
            for illness, score in results.items():
                st.metric(label=f"{illness}",value=f"{int(score)}%", delta=f"{random.randrange(-25,25)}",delta_color='normal')
            # print(results)
            import pandas as pd

            data_df = pd.DataFrame(
                {
                    "percent": list(results.values()),
                }
            )
            st.data_editor(
                    data_df,
                    column_config={
                        "percent": st.column_config.ProgressColumn(
                            "Результаты процентов",
                            help="The sales volume in USD",
                            format='%f',
                            min_value=0,
                            max_value=100,
                        ),
                    },
                    hide_index=True,
                    use_container_width=True,
                    num_rows='fixed'
                )