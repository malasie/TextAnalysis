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

    unwanted_pos = ["SYM", "NUM", "PUNCT", "INTJ", "AUX"]
    words=[]
    for token in text:
        if len(token)>1:
            if token.pos_ not in unwanted_pos and not token.is_stop:
                words.append(token.lemma_)
    
    words = [w for w in words if w.lower() not in stopwords]
    
    return words


#%%
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
    max_freq = max(map(max, freq.values()))
    print(max_freq)
    lim= 100
    sum_freq = np.array(list(map(sum, freq.values())))
    sum_freq = sum_freq[sum_freq>0.1*max(sum_freq)]
    mean = np.mean(sum_freq)
    directions=[[-1,1],[1,1],[1,-1],[-1,-1]]

    for word in freq.keys():
        #grupa startowa
        if sum(freq[word])>max(sum_freq)*0.10:
            x=0
            y=0
            for i in range(4):
                x += directions[i][0]*freq[word][i]
                y += directions[i][1]*freq[word][i]
            
          
            if sum(freq[word])>mean:
                if sum(freq[word])>np.mean(sum_freq[sum_freq>mean]):
                    x = 20/sum(freq[word])
                    y = 20/sum(freq[word])
                else:
                    x = 100/sum(freq[word])
                    y = 100/sum(freq[word])
            else:
                x = 200/sum(freq[word])
                y = 200/sum(freq[word])
            
            if abs(x)>lim or abs(y)>lim:
                print('Potrzebne')
            if x>lim:
                x= lim
            elif x<-lim:
                x=-lim
            if y> lim:
                y= lim
            elif y<-lim:
                y= -lim
            wspol[word]=[x,y]
               
        
'''
come [22, 23, 17, 16] -2 -12
day [13, 18, 34, 19] -20 22
dog [4, 35, 0, 3] -28 -36
say [44, 107, 65, 49] -79 -37
little [33, 35, 26, 15] -13 -27
time [20, 27, 54, 34] -27 41
'''  
        
        

    x = np.transpose(list(wspol.values()))[0]
    y = np.transpose(list(wspol.values()))[1]
    n = wspol.keys()

    fig, ax = plt.subplots()
    ax.scatter(x,y)
    
    for i, txt in enumerate(n):
        ax.annotate(txt, (x[i], y[i]))
    
    plt.xlim(-lim, lim)
    plt.ylim(-lim, lim)
    plt.show()
    
    return freq,wspol

freq,wspol=plot('The Stranger - Albert Camus.pdf')        

#%%

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