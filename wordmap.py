import spacy
from PyPDF2 import PdfReader
import os

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np


def extract_information(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfReader(f)
        information = pdf.metadata
        number_of_pages = len(pdf.pages)
    
    return information, number_of_pages 


extract_information("pdf.pdf")

#%%
def read_page(pdf_path, page):
    reader = PdfReader(pdf_path)
    page = reader.pages[page]
    
    return page.extract_text()



def text_preparation(text, language='english'):   

        
    if language=='english':
        nlp = spacy.load("en_core_web_sm")
        stopwords = ['ing', 'let', 'away']
        
    text = nlp(text)

    unwanted_pos = ["sym", "num", "punct", "intj", "aux"]
    words=[]
    for token in text:
        if len(token)>1:
            if token.pos_ not in unwanted_pos and not token.is_stop:
                words.append(token.lemma_)
    
    words = [w for w in words if w.lower() not in stopwords]
    
    return words

def plot(pdf_path, language='english', filename='', path=''):
    
    information, number_of_pages = extract_information(pdf_path)
    section_list=[]
    section = [0, round(number_of_pages/4),round(number_of_pages/4)*2,round(number_of_pages/4)*3,number_of_pages]
    
    for i in range(1,5):
        word_list=[]
        for page in range(section[i-1], section[i]):
            text = read_page(pdf_path, page)
            word_list.extend(text_preparation(text, language))
        section_list.append(word_list)
     
    freq ={}

    for i in range(len(section_list)):
        for word in section_list[i]:
            if word in freq.keys():
                freq[word][i]+=1
            else:
                freq[word]=[0,0,0,0]
                freq[word][i]+=1
                
    wspol={}
    max_freq=sum(max(freq.values()))
    for word in freq.keys():
        x=10
        y=10
        
        if freq[word][0]>max_freq*0.05:
            x -= (11-freq[word][0]/max_freq)
            y += (11-freq[word][0]/(max_freq))
            
        if freq[word][1]>max_freq*0.05:
            x += (11-freq[word][1]/(max_freq))
            y += (11-freq[word][1]/(max_freq))
            
        if freq[word][2]>max_freq*0.05:
            x += (11-freq[word][2]/(max_freq))
            y -= (11-freq[word][2]/(max_freq))
        if freq[word][3]>max_freq*0.05:
            x -= (11-freq[word][3]/(max_freq))
            y -= (11-freq[word][3]/(max_freq))
            
        if x>20:
            x=20
        if y>20:
            y=20
        if x<0:
            x=0
        if y<0:
            y=0
        wspol[word]=[x,y]
        

    x = np.transpose(list(wspol.values()))[0]
    y = np.transpose(list(wspol.values()))[1]
    n = wspol.keys()

    fig, ax = plt.subplots()
    ax.scatter(x,y)

    for i, txt in enumerate(n):
        ax.annotate(txt, (x[i], y[i]))
    
    plt.show()
    

        

def wordCloud(word_list, info='', filename='', path='', width = 500, height = 300, background = "white",
               colormap = "magma"):
    
    wordcloud = WordCloud(width = width, height = height,
               colormap = colormap, background_color=background).generate(" ".join(word_list))
    
    page, ax = plt.subplots(nrows = 1, ncols = 1, dpi = 300, 
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
            
            
def program(pdf_path, language='english', filename='', path='', width = 500, height = 300, background = "white",
               colormap = "magma"):
    
    languages=['english']
    
    if language.lower() not in languages:
        language='english'
        print("Language not avaible. Language set to English.")
        
    information, number_of_pages = extract_information(pdf_path)
    plot(pdf_path, language='english', filename='', path='')
   
#%%
program('The Stranger - Albert Camus.pdf', filename="stranger", colormap = "viridis")