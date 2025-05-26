import sys
import os
import pytest
from backend.app import news_store, store
from config import STUDENT_ID

# Додати шлях до кореня проєкту
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root)

# Автоматичне очищення стану між тестами
@pytest.fixture(autouse=True)
def clear_stores():
    news_store[STUDENT_ID] = []
    store[STUDENT_ID] = []
    yield
