'''The starting of the program'''
import os
import webbrowser
import subprocess
import shlex
import sys


def main():
    '''main func'''
    print("=== Tournament Optimized-standings ===\n")

    print("Введи повний шлях до CSV файлу:")
    raw_input = input("Шлях: ").strip()

    input_datafile = raw_input.strip('"').strip("'")
    path = os.path.abspath(input_datafile)

    if not os.path.exists(path):
        print(f"Помилка: Файлу '{path}' не існує.")
        return
    if not os.path.isfile(path):
        print(f"Помилка: '{path}' не є файлом.")
        return

    host_data_dir = os.path.dirname(path)
    csv_filename = os.path.basename(path)

    local_output_dir = os.path.join(os.getcwd(), 'output')
    os.makedirs(local_output_dir, exist_ok=True)

    container_data_dir = "/app/data"
    container_frames_dir = "/app/frames"

    print(f"Вхідний файл: {csv_filename}")
    print("Створюю Docker image")

    build_cmd = 'docker build -t standings .'
    try:
        subprocess.run(shlex.split(build_cmd), check=True)
    except subprocess.CalledProcessError:
        print("Помилка створення Docker образу.")
        return

    run_cmd = (
        f'docker run --rm '
        f'-p 8501:8501 '
        f'-e CSV_FILENAME="{csv_filename}" '
        f'-v "{host_data_dir}":"{container_data_dir}":ro '
        f'-v "{local_output_dir}":"{container_frames_dir}" '
        f'standings')

    print("Запускаю веб-сайт")
    print(f"Технічна команда: {run_cmd}\n")
    print("Зачекайте 3-5 секунд, поки сервер запуститься")

    try:
        print('http://localhost:8501')
    except KeyboardInterrupt:
        print("Зупинка роботи...")
    except subprocess.CalledProcessError as e:
        print(f"Помилка Docker: {e}")

if __name__ == "__main__":
    main()
