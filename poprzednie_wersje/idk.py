import spacy
from PyPDF2 import PdfReader
import os

from wordcloud import WordCloud
import matplotlib.pyplot as plt



def extract_information(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfReader(f)
        information = pdf.metadata
        number_of_pages = len(pdf.pages)
    
    return information, number_of_pages 


extract_information("pdf.pdf")[0]

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



def wordCloud(clusters, info='', filename='', path='', width = 500, height = 300, background = "white",
               colormap = "magma"):
    
    order=[0,4,1,7,8,5,3,6,2]
    colormaps=["winter", "winter", "winter", "winter", "cool", "cool", "cool","cool", "plasma"]
    wordclouds=[]
    for i in range(9):
        if len(clusters[order[i]])>0:
            wordclouds.append(WordCloud(width = width, height = height,
                   colormap = colormaps[order[i]], background_color=background).generate(" ".join(clusters[order[i]])))
        else: wordclouds.append(0)       
    
    
    page = plt.figure(figsize=(20,15))
    for i in range(9):    
        im = page.add_subplot(3, 3, i+1)
        im.axis("off")
        if wordclouds[i]!=0:
            im.imshow(wordclouds[i], interpolation='bilinear')

    if info!='':
        page.suptitle(info.author+', '+'"'+info.title+'"', fontsize=36)
    plt.show()
    
    if filename!='':
        if path!='':
            if not os.path.isdir(path):
                os.makedirs(path)
            
            page.savefig('{path}/{name}.jpg'.format(path = path, name = filename))
        else:
            page.savefig('{name}.jpg'.format(name = filename))
            
            
def program(pdf_path, language='english', filename='', path='', width = 1000, height = 600, background = "white",
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
    
    wordCloud(clusters, information, filename, path, width, height, background, colormap)


   
#%%
program('Ecology and Evolution - 2021 - Shetty - pyResearchInsights An open‐source Python package for scientific text analysis.pdf', filename="stranger", colormap = "viridis")

