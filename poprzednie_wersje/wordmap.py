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
    
    sum_freq = np.array(list(map(sum, freq.values())))
    
    directions=[[-1,1],[1,1],[1,-1],[-1,-1]]
    mean = np.mean(sum_freq)
    min_words=max(sum_freq)*0.10
    
    for word in freq.keys():
        #grupa startowa
        nr_words=sum(freq[word])
        if nr_words>=min_words:
            step_x=0
            step_y=0
            for i in range(4):
                step_x += directions[i][0]*freq[word][i]/nr_words
                step_y += directions[i][1]*freq[word][i]/nr_words

            
            if sum(freq[word])>=mean:
                if sum(freq[word])>=np.mean(sum_freq[sum_freq>=mean]):
                    lim_up=max(sum_freq)
                    lim_low=np.mean(sum_freq[sum_freq>=mean])
                    n=10
                    
                else:
                    lim_up = np.mean(sum_freq[sum_freq>=mean])
                    lim_low = mean
                    n=25
                    
            else:
                lim_up=mean
                lim_low =min_words
                n=50
                
            
            x=n*step_x 
            y=n*step_y
            if step_x>0:
                x+=(lim_up-nr_words)/(lim_up-lim_low)*n
            elif step_x<0:
                x-=(lim_up-nr_words)/(lim_up-lim_low)*n
            if step_y>0:
                y+=(lim_up-nr_words)/(lim_up-lim_low)*n
            elif step_y<0:
                y-=(lim_up-nr_words)/(lim_up-lim_low)*n
          
            
            wspol[word]=[x,y]
               
        

    x = np.transpose(list(wspol.values()))[0]
    y = np.transpose(list(wspol.values()))[1]
    n = wspol.keys()

    fig, ax = plt.subplots()
    ax.scatter(x,y)
    
    for i, txt in enumerate(n):
        ax.annotate(txt, (x[i], y[i]))
    plt.plot([-mean,mean],[mean,mean],'y--')
    plt.plot([mean,mean],[-mean,mean],'y--')
    plt.plot([-mean,-mean],[-mean,mean],'y--')
    plt.plot([-mean,mean],[-mean,-mean],'y--')
    mean2=np.mean(sum_freq[sum_freq>=mean])
    plt.plot([-mean2,mean2],[mean2,mean2],'r--')
    plt.plot([mean2,mean2],[-mean2,mean2],'r--')
    plt.plot([-mean2,-mean2],[-mean2,mean2],'r--')
    plt.plot([-mean2,mean2],[-mean2,-mean2],'r--')
    plt.show()
    
    return freq,wspol

freq,wspol=plot('nlp.pdf')        

#%%

def wordCloud(word_list, info='', filename='', path='', width = 500, height = 500, background = "white",
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
#program('The Stranger - Albert Camus.pdf', filename="stranger", colormap = "viridis")