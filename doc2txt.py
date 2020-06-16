import os
import sys
import re

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

def text2str(path, delimiter='.'):
    file = open(path, 'r')
    unparsed_info = file.read()
    element_list = [] # Make an empty list

    for elements in unparsed_info.split(delimiter):
        e = elements.strip(delimiter)
        if e != '':
		    
            element_list.append(e.replace('\n','')) #Append to list
    
    return element_list

def normalization(path, delimiter='.'):
    '''
    Each line is a complete phrase
    '''
    file_input = open(path, 'r')

    #print(file_input)
    file_name, file_extension = os.path.splitext(os.path.basename(path))

    unparsed_info = file_input.read()

    file_output = open(file_name + "_nomalized" + file_extension, 'w')
    #print(unparsed_info)
    bc_text = ' '.join(unparsed_info.split('\n'))
    
    sentenceSplit = filter(None, bc_text.split("."))
    
    for s in sentenceSplit :
        #print(s)
        #print(s.strip() + ".")
        file_output.write(s.strip() + ".\n")

def Find(string): 
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)       
    return [x[0] for x in url]

def purge_urls(path):
    file_name, file_extension = os.path.splitext(os.path.basename(path))

    file_input = open(path, 'r')

    file_output = open(file_name + '_purged.txt', 'w')
    file_index = open(file_name + '_index.txt', 'w')

    unparsed_info = file_input.read().replace('-\n', '')
    #print(unparsed_info)
    index_count = 1

    urls = Find(unparsed_info)

    for element in unparsed_info.splitlines():
        urls = Find(element)
        if len(urls) != 0:
            for url in urls:
                element = element.replace(url, str(index_count), 1)
                file_index.write(str(index_count) + ' - ' + url + '\n')
                index_count = index_count + 1

        char_presence = re.search('[a-zA-Z]', element)
        chapter_present = re.search(r'^\d{1,}\.', element) 

        if char_presence and not chapter_present:
            file_output.write(element + '\n')


    file_output.close()
    file_input.close()
    file_index.close()

    normalization(file_name + '_purged.txt')

if __name__ == "__main__":
    #doc2txt(sys.argv[1:])
    #normalization(sys.argv[1])
    purge_urls(sys.argv[1])