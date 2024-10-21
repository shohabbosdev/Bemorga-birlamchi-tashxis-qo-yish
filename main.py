import json
import streamlit as st

st.set_page_config(page_title="Экспертная система ранней диагностики", page_icon="💊", layout="wide", initial_sidebar_state="expanded")

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

# Load JSON data (familiya, ism, shariflar)
with open('datas.json', 'r', encoding='utf-8') as file:
    patient_data = json.load(file)

# Extract full names from JSON
patient_names = [f"{item['familiya']} {item['ism']} {item['sharifi']}" for item in patient_data]

# UI for patient diagnosis
st.title("💥 Экспертная система ранней диагностики")


col1, col2 = st.columns(2)
with col1:
    with col1.container(border=True):
        # Patient information (select from JSON file)
        selected_name = st.selectbox("Выберите пациента", patient_names)
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
            # Add the rest of the symptoms from the table here...
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
    
import random
with col2:
    with col2.container(border=True):
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
