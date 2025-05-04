import streamlit as st
import pandas as pd
import os

# Подключаем стили
style_path = os.path.join(os.path.dirname(__file__), "..", "styles.css")
with open(style_path, encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Заглушка для данных штабелей
def get_shabels_data():
    # Имитируем данные, которые должны быть в базе данных
    shabel_data = [
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
    ]

    # Преобразуем список в DataFrame
    return pd.DataFrame(shabel_data)

# Шапка как на главной
st.markdown("""
<div class="site-header">
    <div class="logo">🔥 FireWatch</div>
    <div class="nav">
        <a class="nav-item" href="/">Главная</a>
        <a class="nav-item active" href="/shabeli">Штабели</a>
        <a class="nav-item" href="#">Отчёты</a>
        <a class="nav-item" href="#">Справка</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Заголовок + кнопка загрузки
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; margin-top: 20px;">
    <h1>Список штабелей</h1>
    <label for="fileUpload" style="
        background-color: #ff7f2a;
        color: white;
        border: none;
        padding: 10px 24px;
        font-size: 16px;
        border-radius: 8px;
        cursor: pointer;
    ">Загрузить</label>
</div>
""", unsafe_allow_html=True)

# Виджет загрузки файла (спрятан по стилю, но работает)
uploaded_file = st.file_uploader("Загрузить файл", type=["csv", "xlsx"], key="fileUpload", label_visibility="collapsed")


# Отображение содержимого
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Поддерживаются только .csv и .xlsx файлы")
            df = None

        if df is not None:
            st.success("Файл успешно загружен ✅")
            st.dataframe(df)
    except Exception as e:
        st.error(f"Ошибка при загрузке файла: {e}")


# Инфо-блок
st.markdown("""
<div class="info-card">
    Здесь вы найдете информацию по каждому штабелю. Вы можете загрузить файл со списком штабелей в формате CSV или Excel.
</div>
""", unsafe_allow_html=True)


# Загружаем данные штабелей из заглушки
df_shabels = get_shabels_data()

# Отображаем таблицу с данными
st.subheader("Список штабелей")

for _, row in df_shabels.iterrows():
    st.markdown(f"""
    <div style="margin: 10px 0; padding: 15px; background-color: #fff; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
        <a href="/shabel_detail?shabel_id={row['ID']}" style="text-decoration: none; color: #111;">
            <strong>{row['Название']}</strong> — сформирован: {row['Сформирован']}, ближайшее возгорание: {row['Ближайшее возгорание']}, макс. температура: {row['Макс. температура']}
        </a>
    </div>
    """, unsafe_allow_html=True)

# Кнопка для скачивания таблицы в формате CSV
csv = df_shabels.to_csv(index=False)  # Преобразуем таблицу в CSV
st.download_button(
    label="Скачать таблицу штабелей",
    data=csv,
    file_name="shabeli.csv",
    mime="text/csv"
)
