import streamlit as st
import pandas as pd
import os
import datetime


# Заглушка данных
def get_shabels_data():
    return pd.DataFrame([
        {"ID": 1, "Название": "Штабель 1", "Сформирован": "2023-04-01", "Ближайшее возгорание": "2023-05-10",
         "Макс. температура": "450°C"},
        {"ID": 2, "Название": "Штабель 2", "Сформирован": "2023-04-15", "Ближайшее возгорание": "2023-06-20",
         "Макс. температура": "500°C"},
        {"ID": 3, "Название": "Штабель 3", "Сформирован": "2023-05-01", "Ближайшее возгорание": "2023-07-30",
         "Макс. температура": "480°C"},
        {"ID": 4, "Название": "Штабель 4", "Сформирован": "2023-06-05", "Ближайшее возгорание": "2023-08-25",
         "Макс. температура": "470°C"},
        {"ID": 5, "Название": "Штабель 5", "Сформирован": "2023-06-10", "Ближайшее возгорание": "2023-09-12",
         "Макс. температура": "460°C"}
    ])


# Настройки страницы
st.set_page_config(page_title="FireWatch", page_icon="🔥", layout="wide")

# Подключаем стили
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Шапка сайта
def header():
    st.markdown("""
    <div class="site-header">
        <div class="logo">🔥 FireWatch</div>
        <div class="nav">
            <a class="nav-item" href="/">Главная</a>
            <a class="nav-item" href="/stack">Штабели</a>
            <a class="nav-item" href="/warehouse">Склады</a>
            <a class="nav-item" href="/shipments">Выгрузки и отгрузки</a>
            <a class="nav-item" href="/location">Местоположение</a>
            <a class="nav-item" href="#">Отчёты</a>
            <a class="nav-item" href="/help">Справка</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

header()

# Загружаем данные
df = get_shabels_data()

# Получаем сегодняшний день
today = datetime.date.today()


# Генерация данных о самовозгорании (для примера)
def generate_fire_prediction_days(year, month):
    fire_days = [10, 15, 22]  # Пример данных
    return fire_days


# Заголовок страницы
st.title("Предсказание воспламенения дня")
st.markdown("""
<hr style="border: 1px solid #e0e0e0; margin: 20px 0;">
""", unsafe_allow_html=True)

# Получаем параметры даты из URL
params = st.query_params
day = params.get("day", today.day)
month = params.get("month", today.month)
year = params.get("year", today.year)

# Отображаем выбранную дату
selected_date = datetime.date(int(year), int(month), int(day))
st.subheader(f"Дата: {selected_date.strftime('%d.%m.%Y')}")

# Заглушка данных о штабелях, которые могут загореться в этот день
def get_fire_predictions_for_day(date):
    # В реальном приложении здесь будет запрос к базе данных
    return [
        {"id": 5, "name": "Штабель 1", "warehouse": 5},
        {"id": 2, "name": "Штабель 5774", "warehouse": 4},
        {"id": 7, "name": "Штабель 3", "warehouse": 2}
    ]

# Получаем список штабелей, которые могут загореться
fire_predictions = get_fire_predictions_for_day(selected_date)

# Отображаем список штабелей
st.subheader("Список штабелей, которые могут загореться:")
for i, stack in enumerate(fire_predictions, 1):
    st.markdown(f"""
    <div style="margin: 10px 0; padding: 10px; background-color: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <a href="/shabel_detail?shabel_id={stack['id']}" style="text-decoration: none; color: inherit;">
            {i}. {stack['name']} (id {stack['id']}). Склад {stack['warehouse']}
        </a>
    </div>
    """, unsafe_allow_html=True)
