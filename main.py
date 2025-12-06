'''
Organise and orchestrate the program
'''
import subprocess

def main():
    '''
    Docstring for main
    '''
    subprocess.run(["python", "implementation/visual.py"], check = True)

if __name__ == "__main__":
    main()
