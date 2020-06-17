# doc2txt
This small package aims to convert several file formats into ```.txt``` files.
As arguments for the command line you can insert:
- file (or files) path -> the file is converted in ```.txt``` format with the same name
- folder (or folders) path -> all the files in the folder are converted in ```.txt``` format with the same file name
### Installation
This package runs on Ubuntu/Debian. In order to use the textract library we need to install the following dependencies libraries:
```
apt-get install python-dev libxml2-dev libxslt1-dev antiword unrtf poppler-utils pstotext tesseract-ocr \
flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig
```
And then we can install textract through pip:
```
pip install textract
```
### Future work
Add a docker file to make doc2txt usable anywhere.
NB: It may also be necessary to install ```zlib1g-dev``` on Docker instances of Ubuntu.

### Usage
Example of usage:
```
python doc2txt.py <path_to_file>
```
or:
```
python doc2txt.py <path_to_folder>
```
