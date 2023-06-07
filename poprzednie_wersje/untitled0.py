
import numpy as np
import matplotlib.pyplot as plt

lim=100
freq={}
#%%
sum_freq = np.array(list(map(sum, freq.values())))
min_words=np.max(sum_freq)*0.10
mean = np.mean(sum_freq[sum_freq>=min_words])
cord={}
for word in freq.keys():
    if sum(freq[word])>=min_words:
        if sum(freq[word])>=mean:
            if sum(freq[word])>=np.mean(sum_freq[sum_freq>=mean]):
                lim_up=np.max(sum_freq)
                lim_low=np.mean(sum_freq[sum_freq>=mean])
                up = 10
                low = 20
            else:
                lim_up = np.mean(sum_freq[sum_freq>=mean])
                lim_low = mean
                up = 25
                low = 45
        else:
            lim_up = mean
            lim_low = min_words
            up = 50
            low = 100
            
            
        if freq[word].index(max(freq[word]))==0:
            if freq[word][1]>freq[word][3]:
               x=-low* (freq[word][0]-freq[word][1])/(freq[word][0]+freq[word][1])
               y = up+(low-up)*(lim_up-sum(freq[word]))/(lim_up-lim_low)
               
          
            elif freq[word][1]<freq[word][3]:
                y=low* (freq[word][0]-freq[word][3])/(freq[word][0]+freq[word][3])
                x = -up-(low-up)*(lim_up-sum(freq[word]))/(lim_up-lim_low)
                
            else:
                x = -up-(low-up)*(lim_up-sum(freq[word]))/(lim_up-lim_low)
                y = up+(low-up)*(lim_up-sum(freq[word]))/(lim_up-lim_low)
                
        elif freq[word].index(max(freq[word]))==1:
            if freq[word][0]>freq[word][2]:
               x= low* (freq[word][1]-freq[word][0])/(freq[word][1]+freq[word][0])
               y = up+(low-up)*(lim_up-sum(freq[word]))/(lim_up-lim_low)
               
            
            elif freq[word][0]<freq[word][2]:
                y = low* (freq[word][1]-freq[word][2])/(freq[word][1]+freq[word][2])
                x = up+(low-up)*(lim_up-sum(freq[word]))/(lim_up-lim_low)
                
            else:
                x = up+(low-up)*(lim_up-sum(freq[word]))/(lim_up-lim_low)
                y = up+(low-up)*(lim_up-sum(freq[word]))/(lim_up-lim_low)
                
        elif freq[word].index(max(freq[word]))==2:
            if freq[word][1]>freq[word][3]:
               x= low* (freq[word][2]-freq[word][1])/(freq[word][2]+freq[word][1])
               y = -up-(low-up)*(lim_up-sum(freq[word]))/(lim_up-lim_low)
               
            
            elif freq[word][1]<freq[word][3]:
                y = -low* (freq[word][2]-freq[word][3])/(freq[word][2]+freq[word][3])
                x = up+(low-up)*(lim_up-sum(freq[word]))/(lim_up-lim_low)
                
            else:
                x = up+(low-up)*(lim_up-sum(freq[word]))/(lim_up-lim_low)
                y = -up-(low-up)*(lim_up-sum(freq[word]))/(lim_up-lim_low)
        else:
            if freq[word][0]>freq[word][2]:
               x= -low* (freq[word][3]-freq[word][0])/(freq[word][3]+freq[word][0])
               y = -up-(low-up)*(lim_up-sum(freq[word]))/(lim_up-lim_low)
               
            
            elif freq[word][0]<freq[word][2]:
                y = -low* (freq[word][3]-freq[word][2])/(freq[word][3]+freq[word][2])
                x = -up-(low-up)*(lim_up-sum(freq[word]))/(lim_up-lim_low)
                
            else:
                x = -up-(low-up)*(lim_up-sum(freq[word]))/(lim_up-lim_low)
                y = -up-(low-up)*(lim_up-sum(freq[word]))/(lim_up-lim_low)
        cord[word]=[x,y]


x = np.transpose(list(cord.values()))[0]
y = np.transpose(list(cord.values()))[1]
n = cord.keys()

fig, ax = plt.subplots()
ax.scatter(x,y)

for i, txt in enumerate(n):
    ax.annotate(txt, (x[i], y[i]))