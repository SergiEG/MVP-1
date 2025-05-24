import sys, os

# добавляем корень проекта (на уровень выше папки ui) в PYTHONPATH
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from agents.architect import ArchitectAgent
import streamlit as st
# ...

import streamlit as st
from agents.architect import ArchitectAgent

st.set_page_config(
    page_title="MVP-1: Агент-Архитектор",
    layout="wide",
)

st.title("🧱 MVP-1: Агент-Архитектор")
st.markdown("Введите команду ниже и агент выполнит её.")

agent = ArchitectAgent()

# Форма для ввода команды — при отправке поля очищаются автоматически
with st.form("cmd_form", clear_on_submit=True):
    user_input = st.text_input("Ваша команда:")
    submitted = st.form_submit_button("Отправить")

if submitted and user_input:
    # Обработка команды
    response = agent.respond_to_command(user_input)
    st.success(f"Ответ агента: {response}")

# Кнопка «Показать задачи»
if st.button("📋 Показать задачи"):
    tasks = agent.list_tasks()
    st.markdown("**Список задач:**")
    for task in tasks:
        st.write(f"- {task}")

# Кнопка «Показать память»
if st.button("🧠 Показать память"):
    memory = agent.show_memory()
    st.markdown("**Память агента:**")
    for entry in memory:
        # entry = (timestamp, command)
        ts, cmd = entry
        st.write(f"- {ts} — {cmd}")

# Диагностика
if st.button("🔍 Диагностика"):
    diag = agent.run_diagnostic()
    st.success(diag)
