import subprocess

def package_installation():
    apt = "sudo apt "
    pip = "pip "
    ins = "install "
    packages = "python-pip python-dev libxml2-dev libxslt1-dev antiword unrtf poppler-utils pstotext tesseract-ocr flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig"

    print("[+] Installation of the ubuntu packages is starting:")

    for items in packages.split():
        command = str(apt) + str(ins) + str(items)

        subprocess.run(command.split())
        print("\t[+] Package [{}] Installed".format(str(items)))

    text = 'textract'
    command = str(pip) + str(ins) + str(text)
    subprocess.run(command.split())
    print("\t[+] Package textract Installed")

if __name__ == "__main__":
    package_installation()
