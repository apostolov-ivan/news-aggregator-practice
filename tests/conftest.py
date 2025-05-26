import sys
import os
import pytest

# Додати абсолютний шлях до кореня проєкту
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

# Тепер імпорти мають працювати
from backend.app import news_store, store
from config import STUDENT_ID

# Фікстура для очищення даних перед кожним тестом
@pytest.fixture(autouse=True)
def clear_stores():
    news_store[STUDENT_ID] = []
    store[STUDENT_ID] = []
    yield
