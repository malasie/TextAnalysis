from PyPDF2 import PdfReader
import os

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
#nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer

import re
 

'''

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

nltk.download('wordnet')
'''
#%%%


def extract_information(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfReader(f)
        information = pdf.metadata
        number_of_pages = len(pdf.pages)

    txt = f"""
    Information about {pdf_path}: 

    Author: {information.author}
    Creator: {information.creator}
    Producer: {information.producer}
    Subject: {information.subject}
    Title: {information.title}
    Number of pages: {number_of_pages}
    """
    
    return information, number_of_pages 


extract_information("pdf.pdf")
#%%
def read_page(pdf_path, page):
    reader = PdfReader(pdf_path)
    page = reader.pages[page]
    
    return page.extract_text()



def text_preparation(text, language='english'):
    words = nltk.word_tokenize(text)



    words2=[]
    for word in words:
        if len(word)>1:
            if word.isalpha():
                words2.append(word)
            elif re.fullmatch(r'[A-Za-z]+\..[A-Za-z\.]+', word ):
                if word[-1]=='.':
                    word = word[0:-1]
                words2.append(word)
            elif  re.fullmatch(r'[A-Za-z]+-.[A-Za-z]+', word ):
                words2.append(word)
            
    
    
    stopwords = nltk.corpus.stopwords.words(language)
    stopwords.extend(['also', 'yes', 'no','ing', 'u', 'e', 'onto', 'into', 'let', 'around', 'away', 'either', 'neither', 'with', 'without', 'really'])
    words = [w for w in words2 if w.lower() not in stopwords]

    
    lemmatizer = WordNetLemmatizer()

    for i in range(len(words)):
        words[i] = lemmatizer.lemmatize(words[i], 'v')
    
    return words



def wordCloud(word_list, info='', filename='', path='', width = 500, height = 300, background = "white",
               colormap = "magma"):
    
    wordcloud = WordCloud(width = width, height = height,
               colormap = colormap).generate(" ".join(word_list))
    
    page, ax = plt.subplots(nrows = 1, ncols = 1, dpi = 100, 
                                   constrained_layout = True)

    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    if info!='':
        page.suptitle(info.author+', '+'"'+info.title+'"')
    plt.show()
    
    if filename!='':
        if path!='':
            if not os.path.isdir(path):
                os.makedirs(path)
        
            page.savefig('{path}/{name}.jpg'.format(path = path, name = filename))
        else:
            page.savefig('{name}.jpg'.format(name = filename))
    

#%%

def program(pdf_path, language='english', filename='', path='', width = 500, height = 300, background = "white",
               colormap = "magma"):
   information, number_of_pages = extract_information(pdf_path)
   word_list=[]
   for page in range(number_of_pages):
       text = read_page(pdf_path, page)
       word_list.extend(text_preparation(text, language))
   wordCloud(word_list, information, filename, path, width, height, background, colormap)
   
#%%
program('The Stranger - Albert Camus.pdf', filename="stranger")


