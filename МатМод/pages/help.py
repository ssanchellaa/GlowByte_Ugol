# pages/help.py
import streamlit as st

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

# Контент страницы справки
st.title("Справка по использованию сайта")

# Инструкция
st.write("""
**FireWatch** — это сайт для предсказания самовозгораний на складах.

### Как использовать сайт?
1. **Главная страница**: отображает календарь с предсказаниями возможных возгораний на разных штабелях.
2. **Штабели**: просмотр различных штабелей и деталей о возгораниях.
3. **Отчёты**: просматривать отчёты о возгораниях.
4. **Справка**: эта страница, где вы можете узнать, как пользоваться сайтом.

### Как использовать календарь?
- Вы можете выбрать год и месяц, чтобы увидеть календарь с предсказаниями самовозгораний.
- В календаре отображаются дни с возможными возгораниями, и вы можете кликнуть на эти дни для подробной информации.
""")
