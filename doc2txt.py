# -*- coding: utf-8 -*-

import os
import sys
import re

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfdocument import PDFNoOutlines

from urlextract import URLExtract
import string

from docx import Document
import json

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
        return do_conversion(input_arg)
    elif os.path.isdir(input_arg):
        for file in os.listdir(input_arg):
            return do_conversion(file)
    else:
        print('The file %s not exists.' % (input_arg))
        sys.exit(2)

def do_conversion(file):
    file_name, file_extension = os.path.splitext(file)

    if file_extension in white_list_extension_files:

        if file_extension == ".docx":
            remove_header_footer(file)

        text_bytes = textract.process(file, encoding='utf-8', extension=file_extension)
        text = text_bytes.decode('utf-8')#.encode('utf-8')

        f = open(file_name + '.txt', 'w')

        try:
            if file_extension == ".pdf":
                text = purge_index(text, file)
        except PDFNoOutlines:
            print("No outline")

        data = purge_urls(text, file_name)
  
        f.write(data)
        f.close()
        return data
    else:
        print('This file extension is not supported. These are the ones supported: ')
        for ext in white_list_extension_files:
            print("%s\n" % (ext))
        sys.exit(2)

def normalization(text, delimiter='.'):
    '''
    Each line is a complete phrase
    '''
    
    unparsed_info = text

    bc_text = ' '.join(unparsed_info.split('\n'))
    
    sentenceSplit = bc_text.split(".")

    final_splitted_sentences = []

    for idx, s in enumerate(sentenceSplit):
        try:
            new_element = re.sub('\s\s+', ' ', s).strip()
            if len(new_element) == 0:
                continue
            if new_element[0].isdigit() or not new_element[0].isalpha():
                final_splitted_sentences[len(final_splitted_sentences)-1] = (final_splitted_sentences[len(final_splitted_sentences)-1] + '  ' + new_element + '  ')#.strip()
                continue
            if len(new_element.split()) == 1:
                final_splitted_sentences[len(final_splitted_sentences)-1] = (final_splitted_sentences[len(final_splitted_sentences)-1] + '  ' + new_element + '  ')#.strip()
                continue
            final_splitted_sentences.append(new_element.strip())

        except IndexError as e:
            print('Index error: ' + str(idx))  
    
    datas = ''
    for s in final_splitted_sentences:
        clean_s = re.sub('\s\s+', ' ', s)
        if len(clean_s.strip()) > 0 and any(c.isalpha() for c in clean_s):
            datas = datas + s + ".\n"
        
#len(test_string.split())
    #file_output.write(datas)
    datas = re.sub(r'[ ]{2,}', '.', datas)
    return re.sub(r'\.+', ".", datas)

def Find(string): 
    extractor = URLExtract()
    urls = extractor.find_urls(string)
    return urls

def purge_urls(text, file_name):
    urls_dict = {}
    file_index = open(file_name + '_urls.json', 'w')

    unparsed_info = text.replace('-\n', '')
    index_count = 1

    urls = Find(unparsed_info)
    
    if len(urls) != 0:
        punctuation = '!"#$%&\'()*+,-.:;<=>?@[\\]^_`{|}~'
        for url in urls:
            unparsed_info = unparsed_info.replace(url.rstrip(punctuation), '[URL_'+str(index_count)+']', 1)
            unparsed_info = unparsed_info + '\n'
            urls_dict['[URL_'+str(index_count)+']'] = url.rstrip(punctuation)
            index_count = index_count + 1

    unparsed_info = re.sub(r'^\d{1,}\.[\s][a-zA-Z]*', '', unparsed_info)

    file_index.write(json.dumps(urls_dict))
    file_index.close()

    data = normalization(unparsed_info)
    
    return punctuation_normalization(data)

def punctuation_normalization(data):

    # remove • unicode and substitute with -
    normalized_data = re.sub('\u2022', '-', data) 

    # remove ‘ ’ unicodes and substitute with '
    normalized_data = re.sub(u"\u2018", "'", normalized_data)
    normalized_data = re.sub(u"\u2019", "'", normalized_data)
    return normalized_data

def purge_index(data, file):

    titles = []

    datas = ''

    fp = open(file, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)
    # Get the outlines of the document.
    outlines = document.get_outlines()

    for (level,title,dest,a,se) in outlines:
        #titles.append(''.join([i for i in title if not i.isdigit() and i != '.']).strip())
        titles.append(title.strip())

    bc_text = ' '.join(data.split('\n'))
    
    #sentenceSplit = bc_text.split(".")

    for title in titles:
        if re.search(title, bc_text, re.IGNORECASE):
            bc_text = re.sub(title, '', bc_text, flags=re.IGNORECASE)

    return bc_text

def remove_header_footer(file):
    
    document = Document(file)

    ''' rimuoviamo header & footer '''
    for i in range(len(document.sections)):
        document.sections[i].header.is_linked_to_previous = True
        document.sections[i].footer.is_linked_to_previous = True

    document.save(os.path.splitext(file)[0] + '.docx') 

if __name__ == "__main__":
    #doc2txt(sys.argv[1:])	
    #normalization(sys.argv[1])	
    convert_to_txt(sys.argv[1])