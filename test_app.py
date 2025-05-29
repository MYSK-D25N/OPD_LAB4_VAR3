import unittest
from io import BytesIO  # Для создания файловых объектов в памяти
from app import app  # Импорт Flask приложения для тестирования

class FlaskAppTestCase(unittest.TestCase):
    # Настройка перед каждым тестом
    def setUp(self):
        app.config['TESTING'] = True  # Включение режима тестирования
        self.app = app.test_client()  # Создание тестового клиента

    # Тест 1: Проверка корректной загрузки главной страницы
    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Upload a text file', response.data)

    # Тест 2: Проверка ошибки при отсутствии загруженного файла
    def test_no_file_uploaded(self):
        response = self.app.post('/', data={})  # Отправка пустого POST запроса
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No file uploaded', response.data)

    # Тест 3: Проверка ошибки при выборе пустого имени файла
    def test_empty_file_selected(self):
        data = {'file': (BytesIO(b''), '')}  # Создание mock файла с пустым именем
        response = self.app.post('/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please select a file', response.data)

    # Тест 4: Проверка успешной обработки файла
    def test_valid_file_upload(self):
        data = {
            'file': (BytesIO(b'hello world hello'), 'test.txt')  # Создание mock файла с тестовым содержимым
        }
        response = self.app.post('/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Most frequent word', response.data)
        self.assertIn(b'hello', response.data)
        self.assertIn(b'2', response.data)

    # Тест 5: Проверка обработки однобуквенных слов
    def test_single_letter_words(self):
        data = {
            'file': (BytesIO(b'a a a b b'), 'single_letters.txt')
        }
        response = self.app.post('/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'a', response.data)  # Эти проверки будут проваливаться при использовании шаблона \w{2,} (строка 25 app.py)
        self.assertIn(b'3', response.data)

    # Тест 6: Проверка обработки пустых файлов
    def test_empty_file_upload(self):
        data = {
            'file': (BytesIO(b''), 'empty.txt')
        }
        response = self.app.post('/', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'File is empty', response.data)

if __name__ == '__main__':
    unittest.main()