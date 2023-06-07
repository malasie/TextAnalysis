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
            
            
def program(pdf_path, language='english', plot=['cloud', 'clouds', 'map'], filename='', path='', width = 500, height = 300, background = "white",
               colormap = "magma"):
    
    languages=['english']
    
    if language.lower() not in languages:
        language='english'
        print("Language not avaible. Language set to English.")
        
    information, number_of_pages = extract_information(pdf_path)
    word_list=[]
    for page in range(number_of_pages):
        text = read_page(pdf_path, page)
        word_list.extend(text_preparation(text, language))
    wordCloud(word_list, information, filename, path, width, height, background, colormap)
   
#%%
program('nlp.pdf', filename="stranger", colormap = "viridis")