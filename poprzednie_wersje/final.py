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
                if not (len(token)==2 and token.lemma_[-1]=='.'):
                    words.append(token.lemma_)
    
    words = [w for w in words if w.lower() not in stopwords]
    
    return words



def wordCloud(word_list,  width = 500, height = 500, background = "white", colormap = "magma"):
   
        
    wordcloud = WordCloud(width = width, height = height,
               colormap = colormap, background_color=background).generate(" ".join(word_list))
    
    page, ax = plt.subplots(nrows = 1, ncols = 1, dpi = 300, 
                                   constrained_layout = True)

    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    
    return page


def wordClouds(section_list, width = 500, height = 500, background = "white", colormap = "magma"):
 
    clusters = [[],[],[],[],[],[],[],[],[]]
    
    for i in range(0,4):
        for word in section_list[i]:
            if word in section_list[(i+2)%4]:
                clusters[8].append(word)
            elif word in section_list[(i+1)%4]:
                if word in section_list[(i+3)%4]:
                    clusters[8].append(word)
                else:
                    clusters[i + 4].append(word)
            elif word in section_list[(i+3)%4]:
                clusters[(i+3)%4 + 4].append(word)
            else:
                clusters[i].append(word)
    order=[0,4,1,7,8,5,3,6,2]
    colormaps=["winter", "winter", "winter", "winter", "cool", "cool", "cool","cool", "plasma"]
    wordclouds=[]
    for i in range(9):
        if len(clusters[order[i]])>0:
            wordclouds.append(WordCloud(width = width, height = height,
                   colormap = colormaps[order[i]], background_color=background).generate(" ".join(clusters[order[i]])))
        else: wordclouds.append(0)       
    
    
    page = plt.figure(figsize=(20,20))
    for i in range(9):    
        im = page.add_subplot(3, 3, i+1)
        im.axis("off")
        if wordclouds[i]!=0:
            im.imshow(wordclouds[i], interpolation='bilinear')
    return page

def wordMap(section_list):
    
     
    freq ={}

    for i in range(len(section_list)):
        for word in section_list[i]:
            if word.lower() in freq.keys():
                freq[word.lower()][i]+=1 
            elif (word[0].upper()+word[1:] in freq.keys()):
                freq[word[0].upper()+word[1:]][i]+=1 
            else:
                freq[word]=[0,0,0,0]
                freq[word][i]+=1
                
    wspol={}
    fontsize=[]
    max_freq = np.max(map(np.max, freq.values()))
    print(max_freq)
    
    sum_freq = np.array(list(map(sum, freq.values())))
    
    directions=[[-1,1],[1,1],[1,-1],[-1,-1]]
    min_words=np.max(sum_freq)*0.15
    mean = np.mean(sum_freq[sum_freq>=min_words])
    
    for word in freq.keys():
        #grupa startowa
        nr_words=sum(freq[word])
        if nr_words>=min_words:
            step_x=0
            step_y=0
            for i in range(4):
                step_x += directions[i][0]*freq[word][i]/nr_words
                step_y += directions[i][1]*freq[word][i]/nr_words
            if step_x==0:
                step_x=0.0001*directions[freq[word].index(np.max(freq[word]))][0]
            if step_y==0:
                step_y=0.0001*directions[freq[word].index(np.max(freq[word]))][1]
            
            if sum(freq[word])>=mean:
                if sum(freq[word])>=np.mean(sum_freq[sum_freq>=mean]):
                    lim_up=np.max(sum_freq)
                    lim_low=np.mean(sum_freq[sum_freq>=mean])
                    n=10
                    fs=20
                    
                else:
                    lim_up = np.mean(sum_freq[sum_freq>=mean])
                    lim_low = mean
                    n=25
                    fs=16
                    
            else:
                lim_up=mean
                lim_low =min_words
                n=50
                fs=10

                
                
            x=n*step_x 
            y=n*step_y
            

            
            if step_x>0:
                x+=(lim_up-nr_words)/(lim_up-lim_low)*n
                if x>n:
                    x=n
            elif step_x<0:
                x-=(lim_up-nr_words)/(lim_up-lim_low)*n
                if x<-n:
                    x=-n
       
                
            if step_y>0:
                y+=(lim_up-nr_words)/(lim_up-lim_low)*n
                if y>n:
                    y=n
            elif step_y<0:
                y-=(lim_up-nr_words)/(lim_up-lim_low)*n
                if y<-n:
                    y=-n
            
          
            
            wspol[word]=[x,y]
            fontsize.append(fs)
               
        
    x = np.transpose(list(wspol.values()))[0]
    y = np.transpose(list(wspol.values()))[1]
    n = wspol.keys()

    fig, ax = plt.subplots(figsize=(12,12))
    ax.scatter(x,y)
    
    for i, txt in enumerate(n):
        ax.annotate(txt, (x[i], y[i]), fontsize=fontsize[i])
        
    plt.plot([-10,10],[10,10],'y--')
    plt.plot([10,10],[-10,10],'y--')
    plt.plot([-10,-10],[-10,10],'y--')
    plt.plot([-10,10],[-10,-10],'y--')
    
    plt.plot([-25,25],[25,25],'r--')
    plt.plot([25,25],[-25,25],'r--')
    plt.plot([-25,-25],[-25,25],'r--')
    plt.plot([-25,25],[-25,-25],'r--')
    
    plt.axis('off')
    
    return fig

          
            
def program(pdf_path, language='english', plot=['Wordcloud', 'section_clouds', 'Wordmap'], filename='', path='', figsize=(45,15), width = 500, height = 500, background = "white",
               colormap = "magma"):
    
    languages=['english']
    
    if language.lower() not in languages:
        language='english'
        print("Language not avaible. Language set to English.")
    
    
    information, number_of_pages = extract_information(pdf_path)
    section_list=[]
    section = [0, round(number_of_pages/4),round(number_of_pages/4)*2,round(number_of_pages/4)*3,number_of_pages]
    
    for i in range(1,5):
        word_list=[]
        for page in range(section[i-1], section[i]):
            text = read_page(pdf_path, page)
            word_list.extend(text_preparation(text, language))
        section_list.append(word_list)
    
    word_list = [word for section in section_list for word in section_list][0]
    
    
    page = plt.figure(figsize=figsize)
    for i, text in enumerate(plot):
        im = page.add_subplot(1,len(plot), i+1)
        im.axis("off")
        if text=='Wordcloud':
            wordCloud(word_list, width, height, background, colormap)
            im.imshow(wordCloud, interpolation='bilinear')
        elif text=='section_clouds':
            wordClouds(section_list, width, height, background, colormap)
            im.imshow(wordClouds, interpolation='bilinear')
        elif text=='Wordmap':
            wordMap(section_list)
            im.imshow(wordClouds, interpolation='bilinear')
    
    if information!='':
        page.suptitle(information.author+', '+'"'+information.title+'"', fontsize=36)
    plt.show()
    
    if filename!='':
        if path!='':
            if not os.path.isdir(path):
                os.makedirs(path)
            
            page.savefig('{path}/{name}.jpg'.format(path = path, name = filename))
        else:
            page.savefig('{name}.jpg'.format(name = filename))
            
   
#%%
program('nlp.pdf', filename="NLP", colormap = "viridis")