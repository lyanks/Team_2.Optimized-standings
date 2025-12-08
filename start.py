import os
import subprocess
import shlex

def main():
    print("Введи повний шлях до файлу:")
    local_file = input("Шлях до файлу: ").strip()

    if not os.path.isfile(local_file):
        print("Файлу не існує! Перевір шлях і спробуй ще раз.")
        return

    local_file = os.path.abspath(local_file)

    print("Створюю Docker image з файлом:")
    print(local_file)

    # Команда docker build
    cmd = f'docker build --build-arg LOCALFILE="{local_file}" -t standings .'
    print(cmd)

    try:
        subprocess.run(shlex.split(cmd), check=True)
    except subprocess.CalledProcessError as e:
        print("Помилка створення Docker образу:")
        print(e)

if __name__ == "__main__":
    main()
