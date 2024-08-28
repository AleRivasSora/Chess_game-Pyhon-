import subprocess

def main():
    subprocess.call(['pyinstaller', '--onefile', 'app.py'])

if __name__ == '__main__':
    main()