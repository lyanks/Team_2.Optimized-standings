'''start of whole program'''
import os
import subprocess
import shlex

def main():
    '''main'''
    print("Введи повний шлях до файлу:")
    input_datafile = input("Шлях до файлу: ").strip()

    # if not os.path.isfile(input_datafile):
    #     print("Файлу не існує! Перевір шлях і спробуй ще раз.")
    #     return

    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f"Файлу '{path}' не існує. Перевірте шлях.")

    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(f"'{path}' не є файлом. Вкажіть коректний файл.")

    if not os.access(path, os.R_OK):
        raise argparse.ArgumentTypeError(f"Файл '{path}' не можна прочитати. Немає дозволу.")

    input_datafile_dir = os.path.dirname(input_datafile)
    input_datafile = os.path.abspath(input_datafile)

    local_output_dir = os.path.join(os.getcwd(), 'output')
    os.makedirs(local_output_dir, exist_ok=True)
    print(f"Результати будуть збережені у локальній теці: {local_output_dir}")

    container_data_dir = "/app/data"
    container_frames_dir = "/app/frames"

    container_input_path = container_data_dir

    print(f"\nСтворюю Docker image... з файлом {input_datafile}")

    build_cmd = 'docker build -t standings .'

    try:
        subprocess.run(shlex.split(build_cmd), check=True)
    except subprocess.CalledProcessError as e:
        print(f"Помилка створення Docker образу. {e}")
        return

    run_cmd = (
        f'docker run --rm '
        '--name standings_proc '
        f'-v "{input_datafile_dir}":"{container_input_path}":ro '
        f'-v "{local_output_dir}":"{container_frames_dir}" '
        f'standings')

    print("\nЗапускаю Docker контейнер...")
    print(f"Команда: {run_cmd}")

    try:
        subprocess.run(run_cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Помилка запуску Docker контейнера:")
        print(e)

    print(f"\n✅ Завершено. Результати (frames) у теці: {local_output_dir}")

    # show visualiztion from output directory


if __name__ == "__main__":
    main()
