import streamlit as st
import pandas as pd
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
            <a class="nav-item" href="/help">Справка</a>  <!-- Ссылка на справку -->
        </div>
    </div>
    """, unsafe_allow_html=True)

header()

# Примерные данные
past_fires = {
    5: [
        {"Название": "Штабель A", "Состояние": "Сгорел полностью"},
        {"Название": "Штабель B", "Состояние": "Повреждён"}
    ],
    12: [
        {"Название": "Штабель C", "Состояние": "Сгорел частично"}
    ],
    17: [
        {"Название": "Штабель D", "Состояние": "Сгорел полностью"},
        {"Название": "Штабель E", "Состояние": "Сгорел частично"},
        {"Название": "Штабель F", "Состояние": "Сгорел полностью"}
    ]
}

future_fires = {}
today = datetime.date.today()
for i in range(1, 4):
    day = (today + datetime.timedelta(days=i)).day
    future_fires[day] = [
        {"Название": f"Штабель {chr(88+i)}", "Прогноз": "Высокий риск"}
        for _ in range(i)
    ]

# Календарь

def render_calendar(year, month):
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    html = f"""
    <div class='calendar-wrapper'>
        <h2 style='text-align: center;'>Календарь предсказания самовозгораний</h2>
        <h3 style='text-align: center;'>{month_name} {year}</h3>
        <table class='calendar'>
    """

    html += "<tr>" + "".join(
        f"<th class='center'>{day}</th>" for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    ) + "</tr>"

    for week in cal:
        html += "<tr>"
        for day in week:
            if day == 0:
                html += "<td class='day empty'></td>"
            else:
                classes = "day"
                label = str(day)
                link = None

                if day == today.day and month == today.month and year == today.year:
                    classes += " today"

                if day in past_fires:
                    count = len(past_fires[day])
                    label += f"<br><span class='fire-count past'>{count} 🔥</span>"
                    link = f"/day?day={day}&month={month}&year={year}&type=past"
                elif day in future_fires:
                    count = len(future_fires[day])
                    label += f"<br><span class='fire-count future'>{count} 🔥</span>"
                    link = f"/day?day={day}&month={month}&year={year}&type=future"

                if link:
                    html += f"<td class='{classes}'><a href='{link}' class='calendar-link'>{label}</a></td>"
                else:
                    html += f"<td class='{classes}'>{label}</td>"
        html += "</tr>"

    html += "</table></div>"
    return html

# Выбор года и месяца
col1, col2 = st.columns([1, 3])
with col1:
    year = st.selectbox("Выберите год", list(range(2000, 2031)), index=today.year - 2000)
with col2:
    month_name_list = list(calendar.month_name)[1:]
    month_name_selected = st.selectbox("Выберите месяц", month_name_list, index=today.month - 1)
    month = month_name_list.index(month_name_selected) + 1

# Отображение календаря
calendar_html = render_calendar(year, month)
st.markdown(calendar_html, unsafe_allow_html=True)

st.markdown("""
<style>
.day.today {
    border: 2px solid red;
    border-radius: 8px;
}
.calendar-link {
    text-decoration: none;
    color: black;
    display: block;
    width: 100%;
    height: 100%;
}
.fire-count {
    display: inline-block;
    padding: 2px 6px;
    border-radius: 12px;
    font-size: 0.8em;
    margin-top: 4px;
}
.fire-count.past {
    background-color: #ffebee;
    color: #d32f2f;
}
.fire-count.future {
    background-color: #fff3e0;
    color: #f57c00;
}
</style>
""", unsafe_allow_html=True)
