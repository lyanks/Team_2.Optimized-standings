'''
Organise and orchestrate the program
'''
import subprocess

def main():
    '''
    Docstring for main
    '''
    path_to_data = input()
    path_to_data = "data/" + path_to_data  # Твоя змінна зі шляхом
    path_to_script = "implementation/visual.py"

    # Передаємо шлях до visual.py як аргумент
    command = ["python", path_to_script, path_to_data]

    try:
        subprocess.run(command, check=True)
        print("Візуалізація успішно завершена.")
    except subprocess.CalledProcessError as e:
        print(f"Помилка при запуску візуалізації: {e}")

if __name__ == "__main__":
    main()
