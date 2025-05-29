# Импорт необходимых библиотек
from flask import Flask, render_template, request  # Основные компоненты Flask
from collections import Counter  # Для подсчета частоты слов
import re  # Регулярные выражения для обработки текста

# Создание экземпляра Flask приложения
app = Flask(__name__)

# Определение маршрута для главной страницы (обрабатывает GET и POST запросы)
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # Обработка POST запроса (отправка формы)
    if request.method == 'POST':
        # Проверка, был ли загружен файл
        if 'file' not in request.files:
            return render_template('index.html', error="Файл не загружен")

        file = request.files['file']

        # Проверка, выбрал ли пользователь файл
        if file.filename == '':
            return render_template('index.html', error="Пожалуйста, выберите файл")

        # Обработка файла, если он существует
        if file:
            try:
                # Чтение и декодирование содержимого файла
                text = file.read().decode('utf-8')
                
                # Нахождение всех слов (используя regex для границ слов)
                words = re.findall(r'\b\w+\b', text.lower())
                # Альтернативная версия, которая игнорирует однобуквенные слова:
                # words = re.findall(r'\b\w{2,}\b', text.lower())

                # Обработка пустых файлов
                if not words:
                    return render_template('index.html', error="Файл пуст")
                
                # Подсчет частоты слов и нахождение наиболее частого
                word_counts = Counter(words)
                most_common = word_counts.most_common(1)[0]  # Получение кортежа (слово, количество)
                return render_template('index.html', most_common=most_common)
            
            except UnicodeDecodeError:
                return render_template('index.html', error="Файл должен быть текстовым")
    
    # Обработка GET запросов или неудачных POST запросов (показ пустой формы)
    return render_template('index.html')

# Запуск приложения, если оно выполняется напрямую
if __name__ == '__main__':
    app.run(debug=True)