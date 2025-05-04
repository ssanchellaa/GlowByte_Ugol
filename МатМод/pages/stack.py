import streamlit as st
import pandas as pd
import os
import datetime

# Настройки страницы
st.set_page_config(page_title="FireWatch", page_icon="🔥", layout="wide")

# Подключаем стили
style_path = os.path.join(os.path.dirname(__file__), "..", "styles.css")
with open(style_path, encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Шапка сайта
def header():
    st.markdown("""
    <div class="site-header">
        <div class="logo">🔥 FireWatch</div>
        <div class="nav">
            <a class="nav-item" href="/">Главная</a>
            <a class="nav-item active" href="/stack">Штабели</a>
            <a class="nav-item" href="/warehouse">Склады</a>
            <a class="nav-item" href="/shipments">Выгрузки и отгрузки</a>
            <a class="nav-item" href="/location">Местоположение</a>
            <a class="nav-item" href="#">Отчёты</a>
            <a class="nav-item" href="/help">Справка</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

header()

# Заглушка для данных штабелей
def get_shabels_data():
    # Имитируем данные, которые должны быть в базе данных
    shabel_data = [
        {"ID": 1, "Название": "Штабель 1", "Сформирован": "2023-04-01", "Ближайшее возгорание": "2023-05-10",
         "Макс. температура": "450°C", "Склад": 5},
        {"ID": 2, "Название": "Штабель 5774", "Сформирован": "2023-04-15", "Ближайшее возгорание": "2023-06-20",
         "Макс. температура": "500°C", "Склад": 4},
        {"ID": 3, "Название": "Штабель 3", "Сформирован": "2023-05-01", "Ближайшее возгорание": "2023-07-30",
         "Макс. температура": "480°C", "Склад": 2},
        {"ID": 4, "Название": "Штабель 4", "Сформирован": "2023-06-05", "Ближайшее возгорание": "2023-08-25",
         "Макс. температура": "470°C", "Склад": 3},
        {"ID": 5, "Название": "Штабель 5", "Сформирован": "2023-06-10", "Ближайшее возгорание": "2023-09-12",
         "Макс. температура": "460°C", "Склад": 1}
    ]

    # Преобразуем список в DataFrame
    return pd.DataFrame(shabel_data)

# Инициализация состояния для хранения штабелей
if 'stacks' not in st.session_state:
    st.session_state.stacks = get_shabels_data()

# Заголовок + форма добавления
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; margin-top: 20px;">
    <h1>Список штабелей</h1>
</div>
""", unsafe_allow_html=True)

# Форма добавления нового штабеля
st.markdown("""
<div style="margin: 20px 0; padding: 15px; background-color: #f8f9fa; border-radius: 8px;">
    <h3>Добавить новый штабель</h3>
</div>
""", unsafe_allow_html=True)

with st.form("new_stack_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        stack_name = st.text_input("Номер штабеля", placeholder="Например: Штабель 1")
    with col2:
        stack_id = st.number_input("ID штабеля", min_value=1, step=1)
    with col3:
        warehouse = st.number_input("Номер склада", min_value=1, step=1)
    
    submit_button = st.form_submit_button("Добавить штабель")
    
    if submit_button:
        if stack_name and stack_id and warehouse:
            # Создаем новый штабель
            new_stack = {
                "ID": stack_id,
                "Название": stack_name,
                "Сформирован": datetime.datetime.now().strftime("%Y-%m-%d"),
                "Ближайшее возгорание": "Не определено",
                "Макс. температура": "Не измерено",
                "Склад": warehouse
            }
            
            # Добавляем новый штабель в список
            new_df = pd.DataFrame([new_stack])
            st.session_state.stacks = pd.concat([st.session_state.stacks, new_df], ignore_index=True)
            st.success("Штабель успешно добавлен!")
        else:
            st.error("Пожалуйста, заполните все поля")

# Фильтры и поиск
st.markdown("""
<div style="margin: 20px 0; padding: 15px; background-color: #f8f9fa; border-radius: 8px;">
    <h3>Фильтры и поиск</h3>
</div>
""", unsafe_allow_html=True)

# Создаем колонки для фильтров
col1, col2, col3 = st.columns(3)

with col1:
    search_query = st.text_input("Поиск по названию", placeholder="Введите название штабеля")

with col2:
    id_filter = st.text_input("Фильтр по ID", placeholder="Введите ID")

with col3:
    warehouse_filter = st.text_input("Фильтр по складу", placeholder="Введите номер склада")

# Применяем фильтры
filtered_df = st.session_state.stacks.copy()

if search_query:
    filtered_df = filtered_df[filtered_df['Название'].str.contains(search_query, case=False, na=False)]

if id_filter:
    filtered_df = filtered_df[filtered_df['ID'].astype(str).str.contains(id_filter)]

if warehouse_filter:
    filtered_df = filtered_df[filtered_df['Склад'].astype(str).str.contains(warehouse_filter)]

# Отображаем отфильтрованный список штабелей
st.markdown("""
<div style="margin: 20px 0; padding: 15px; background-color: #f8f9fa; border-radius: 8px;">
    <h3>Список штабелей</h3>
</div>
""", unsafe_allow_html=True)

for i, (_, row) in enumerate(filtered_df.iterrows(), 1):
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.markdown(f"""
        <div style="margin: 10px 0; padding: 10px; background-color: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <a href="/shabel_detail?shabel_id={row['ID']}" style="text-decoration: none; color: inherit;">
                {i}. {row['Название']} (id {row['ID']}). Склад {row['Склад']}
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Кнопки редактирования и удаления
        edit_key = f"edit_{row['ID']}"
        delete_key = f"delete_{row['ID']}"
        
        col_edit, col_delete = st.columns(2)
        with col_edit:
            if st.button("✏️", key=edit_key):
                st.session_state[f"editing_{row['ID']}"] = True
                st.session_state[f"edit_name_{row['ID']}"] = row['Название']
                st.session_state[f"edit_warehouse_{row['ID']}"] = row['Склад']
        
        with col_delete:
            if st.button("🗑️", key=delete_key):
                st.session_state.stacks = st.session_state.stacks[st.session_state.stacks['ID'] != row['ID']]
                st.rerun()
    
    # Форма редактирования
    if st.session_state.get(f"editing_{row['ID']}", False):
        with st.form(f"edit_form_{row['ID']}"):
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                new_name = st.text_input("Номер штабеля", 
                                       value=st.session_state.get(f"edit_name_{row['ID']}", row['Название']),
                                       key=f"new_name_{row['ID']}")
            with col2:
                new_warehouse = st.number_input("Номер склада", 
                                              min_value=1, 
                                              value=st.session_state.get(f"edit_warehouse_{row['ID']}", row['Склад']),
                                              key=f"new_warehouse_{row['ID']}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Сохранить"):
                    # Обновляем данные штабеля
                    st.session_state.stacks.loc[st.session_state.stacks['ID'] == row['ID'], 'Название'] = new_name
                    st.session_state.stacks.loc[st.session_state.stacks['ID'] == row['ID'], 'Склад'] = new_warehouse
                    st.session_state[f"editing_{row['ID']}"] = False
                    st.rerun()
            with col2:
                if st.form_submit_button("Отмена"):
                    st.session_state[f"editing_{row['ID']}"] = False
                    st.rerun()

# Кнопка для скачивания таблицы в формате CSV
csv = filtered_df.to_csv(index=False)  # Преобразуем таблицу в CSV
st.download_button(
    label="Скачать таблицу штабелей",
    data=csv,
    file_name="stack.csv",
    mime="text/csv"
)
