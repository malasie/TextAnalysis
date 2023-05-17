# cztery klastry im więcej słów, tym bliżej środka. Im więcej wystąpień danego słowa w innym klastrze tym bliżej do tego klastru.

import matplotlib.pyplot as plt
import numpy as np

strona1=['a', 'b', 'c', 'a', 'a','d', 'e', 'f', 'e']
strona2=['a', 'f', 'c', 'a', 'a','g', 'e', 'f', 'f']
strona3=['a', 'z', 'c', 'c', 'c','g', 'e', 'f', 'z']
strona4=['a', 'w','h', 'i', 'i','x','a','d', 'd', 'a']
strony=[strona1, strona2, strona3, strona4]

freq ={}

for i in range(len(strony)):
    for letter in strony[i]:
        if letter in freq.keys():
            freq[letter][i]+=1
        else:
            freq[letter]=[0,0,0,0]
            freq[letter][i]+=1
            
wspol={}

for letter in freq.keys():
    x=5
    y=5
    if freq[letter][0]>0:
        x -= (6-freq[letter][0])
        y += (6-freq[letter][0])
        
    if freq[letter][1]>0:
        x += (6-freq[letter][1])
        y += (6-freq[letter][1])
        
    if freq[letter][2]>0:
        x += (6-freq[letter][2])
        y -= (6-freq[letter][2])
    if freq[letter][3]>0:
        x -= (6-freq[letter][3])
        y -= (6-freq[letter][3])
        
    if x>10:
        x=10
    if y>10:
        y=10
    if x<0:
        x=0
    if y<0:
        y=0
    wspol[letter]=[x,y]
    

x = np.transpose(list(wspol.values()))[0]
y = np.transpose(list(wspol.values()))[1]
n = wspol.keys()

fig, ax = plt.subplots()
ax.scatter(x,y)

for i, txt in enumerate(n):
    ax.annotate(txt, (x[i], y[i]))