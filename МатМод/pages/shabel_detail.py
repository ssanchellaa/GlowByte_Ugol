import streamlit as st
import pandas as pd
import os
import datetime
import calendar

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

# Получение даты из параметров запроса
params = st.query_params
selected_date = params.get("date", "Не указана")



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

# Получение ID штабеля из параметра
try:
    shabel_id = int(params.get("shabel_id", 0))
except:
    shabel_id = 0

df = get_shabels_data()
shabel_row = df[df["ID"] == shabel_id]

if not shabel_row.empty:
    row = shabel_row.iloc[0]
    # Обновленный заголовок
    st.title(f"Штабель {row['Название']}(id{row['ID']})")

    # Информационная рамка
    st.markdown("""
    <div style="padding: 20px; background-color: #ffffff; border-radius: 12px; margin: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
        <h3>Краткая информация:</h3>
        <p><strong>Склад:</strong> {warehouse}</p>
        <p><strong>Ближайшее возгорание:</strong> {fire_date}</p>
        <p><strong>Рекомендации:</strong> перемешать уголь в штабеле</p>
    </div>
    """.format(
        warehouse=row['Склад'] if 'Склад' in row else 'Не указан',
        fire_date=row['Ближайшее возгорание']
    ), unsafe_allow_html=True)

    # Календарь возгорания
    def render_calendar(year, month, fire_prediction_days):
        cal = calendar.monthcalendar(year, month)
        month_name = calendar.month_name[month]
        html = f"<div class='calendar-wrapper'><h3>{month_name} {year}</h3><h4>Календарь предсказания самовозгораний</h4><table class='calendar'>"
        html += "<tr>" + "".join(
            f"<th class='center'>{day}</th>" for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]) + "</tr>"

        for week in cal:
            html += "<tr>"
            for day in week:
                if day == 0:
                    html += "<td class='day empty'></td>"
                else:
                    classes = "day"
                    if day in fire_prediction_days:
                        date_str = datetime.date(year, month, day).isoformat()
                        html += f"<td class='{classes}' style='background-color: #ffebee;'><a href='/fire_details?date={date_str}&shabel_id={shabel_id}' style='text-decoration: none; color: #d32f2f; font-weight: bold;'>{day}</a></td>"
                    else:
                        html += f"<td class='{classes}'>{day}</td>"
            html += "</tr>"
        html += "</table></div>"
        return html

    def generate_fire_prediction_days(year, month):
        # В реальном приложении здесь будет запрос к базе данных
        # Сейчас возвращаем примерные даты
        return [10, 15, 22]

    today = datetime.date.today()
    fire_prediction_days = generate_fire_prediction_days(today.year, today.month)

    col1, col2 = st.columns([1, 3])
    with col1:
        year = st.selectbox("Год", list(range(2000, 2031)), index=today.year - 2000)
    with col2:
        month = st.selectbox("Месяц", list(range(1, 13)), index=today.month - 1)

    st.markdown(render_calendar(year, month, fire_prediction_days), unsafe_allow_html=True)

    # Раздел измерений температуры
    st.markdown("""
    <hr style="border: 1px solid #e0e0e0; margin: 20px 0;">
    """, unsafe_allow_html=True)
    st.subheader("Измерения температуры")

    # Форма добавления измерений
    with st.form("temperature_measurement_form"):
        st.write("Добавить новое измерение:")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            date = st.date_input("Дата акта")
        with col2:
            temperature = st.number_input("Температура (°C)", min_value=0, max_value=1000)
        with col3:
            shift = st.selectbox("Смена", ["1", "2", "3"])
        with col4:
            picket = st.text_input("Пикет")
        
        submit_button = st.form_submit_button("Добавить измерения")
        
        if submit_button:
            # Здесь будет логика сохранения данных
            st.success("Измерения успешно добавлены!")

else:
    st.error("Штабель не найден.")
