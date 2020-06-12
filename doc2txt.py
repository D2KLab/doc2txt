import os
import sys

try:
    import textract
except ImportError:
    print('There is some error occurring when importing the textract library. Please, see the documentation in order to check your installation.')
    sys.exit(1)

white_list_extension_files = ['.csv', '.doc', '.docx', '.eml', '.epub', '.gif', '.htm', '.html', '.jpeg', '.jpg', '.json', '.log', '.mp3', '.msg', '.odt', '.ogg', '.pdf', '.png', '.pptx', '.ps', '.psv', '.rtf', '.tff', '.tif', '.tiff', '.tsv', '.txt', '.wav', '.xls', '.xlsx']

def doc2txt(argv):
    for arg in sys.argv[1:]:
        convert_to_txt(arg)

def convert_to_txt(input_arg):
    if os.path.isfile(input_arg):
        do_conversion(input_arg)
    elif os.path.isdir(input_arg):
        for file in os.listdir(input_arg):
            do_conversion(file)
    else:
        print('The file %s not exists.' % (input_arg))
        sys.exit(2)

def do_conversion(file):
    file_name, file_extension = os.path.splitext(file)

    if file_extension in white_list_extension_files:
        text_bytes = textract.process(file, extension=file_extension)
        text = text_bytes.decode('utf-8')

        f = open(file_name + '.txt', 'w')
        f.write(text)
        f.close()
    else:
        print('This file extension is not supported. These are the ones supported: ')
        for ext in white_list_extension_files:
            print("%s\n" % (ext))
        sys.exit(2)

if __name__ == "__main__":
    doc2txt(sys.argv[1:])

def text2str(path, delimiter='.'):
    file = open(path, 'r')
    unparsed_info = file.read()
    element_list = [] # Make an empty list

    for elements in unparsed_info.split(delimiter):
        e = elements.strip(delimiter)
        if e != '':
		    
            element_list.append(e.replace('\n','')) #Append to list
    
    return element_list