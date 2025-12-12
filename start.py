import os
import subprocess
import shlex
import sys


def main():
    print("=== 🏆 Tournament System Launcher ===\n")
    
    # 1. Запитуємо шлях до файлу
    print("Введи повний шлях до CSV файлу:")
    raw_input = input("Шлях: ").strip()
    
    # Очищаємо шлях від лапок, якщо вони є (Windows часто додає їх)
    input_datafile = raw_input.strip('"').strip("'")
    path = os.path.abspath(input_datafile)

    # 2. Перевірки
    if not os.path.exists(path):
        print(f"❌ Помилка: Файлу '{path}' не існує.")
        return
    if not os.path.isfile(path):
        print(f"❌ Помилка: '{path}' не є файлом.")
        return

    # Отримуємо папку, де лежить файл, та саме ім'я файлу
    host_data_dir = os.path.dirname(path)     # Наприклад: C:/Users/Documents
    csv_filename = os.path.basename(path)     # Наприклад: matches.csv

    # Папка для результатів (куди зберігати картинки, якщо треба)
    local_output_dir = os.path.join(os.getcwd(), 'output')
    os.makedirs(local_output_dir, exist_ok=True)

    # Шляхи всередині Docker контейнера
    container_data_dir = "/app/data"
    container_frames_dir = "/app/frames"

    print(f"\n📂 Вхідний файл: {csv_filename}")
    print(f"🔨 Створюю Docker image...")

    # 3. Build (Збірка образу)
    build_cmd = 'docker build -t standings .'
    try:
        subprocess.run(shlex.split(build_cmd), check=True)
    except subprocess.CalledProcessError:
        print("❌ Помилка створення Docker образу.")
        return

    # 4. Run (Запуск контейнера)
    # ВАЖЛИВО:
    # -p 8501:8501 -> Відкриває порт для сайту
    # -e CSV_FILENAME -> Передає ім'я файлу всередину Python-коду
    # -v ... -> Монтує папку з твоїм файлом у папку /app/data в контейнері
    run_cmd = (
        f'docker run --rm '
        f'-p 8501:8501 '
        f'-e CSV_FILENAME="{csv_filename}" '
        f'-v "{host_data_dir}":"{container_data_dir}":ro '
        f'-v "{local_output_dir}":"{container_frames_dir}" '
        f'standings'
    )

    print("\n🚀 Запускаю веб-сайт...")
    print(f"Технічна команда: {run_cmd}\n")
    print("⏳ Зачекайте 3-5 секунд, поки сервер запуститься...")

    # Спроба відкрити браузер автоматично
    try:
        # Даємо контейнеру трохи часу на старт
        if sys.platform == 'win32':
            # На Windows запускаємо команду і не блокуємо консоль відразу
             subprocess.Popen(['start', 'http://localhost:8501'], shell=True)
        else:
             pass # На Linux/Mac можна додати webbrowser.open пізніше
        
        # Запускаємо сам контейнер (ця команда "зависає", поки працює сайт)
        subprocess.run(run_cmd, shell=True, check=True)

    except KeyboardInterrupt:
        print("\n🛑 Зупинка роботи...")
    except subprocess.CalledProcessError as e:
        print(f"Помилка Docker: {e}")

if __name__ == "__main__":
    main()
