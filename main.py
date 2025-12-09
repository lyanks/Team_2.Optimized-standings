'''
Organise and orchestrate the program
'''
import subprocess
from pathlib import Path

def main():
    '''
    Docstring for main
    '''
    input_dir = Path("//app//data")

    files = [f for f in input_dir.iterdir() if f.is_file()]
    path_to_script = "implementation/visual.py"

    input_file_path_str = files[0].as_posix()

    print(f"Передаю файл для обробки: {input_file_path_str}")

    command = ["python", path_to_script, input_file_path_str]

    try:
        subprocess.run(command, check=True)
        print("Візуалізація успішно завершена.")
    except subprocess.CalledProcessError as e:
        print(f"Помилка при запуску візуалізації: {e}")

if __name__ == "__main__":
    main()
