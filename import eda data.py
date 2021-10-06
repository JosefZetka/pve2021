import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy import polynomial as P
from scipy import interpolate
from datetime import datetime

import pdb
class Record:
    def __init__(self, number_in_row=0, datetime="", pci1=0,pci2=0,pci=0,adtur=0,adcer=0, \
                 dhlad=0, hhlad=0, pdg=0, avyr=0, ndg=0):
        self.number_in_row=number_in_row
        self.datetime = datetime
        self.pci1 = pci1
        self.pci2 = pci2
        self.pci = pci
        self.adtur = adtur
        self.adcer = adcer
        self.dhlad = dhlad
        self.hhlad = hhlad
        self.pdg = pdg
        self.avyr = avyr
        self.ndg = ndg       
       
#data_eda = pd.read_csv('eda.txt',index_col =[0])
data_eds = pd.read_csv('eds.txt',index_col =[0] )
records=list()
best_rec = list()
iterator =0
for index, row in data_eds.iterrows():
    iterator +=1
    #if iterator == 10:
        #print(row)
        #print(f'number_in_row = {iterator}, datetime = {index}, pci1={row[0]}, pci2={row[1]},pci={row[3]},adtur={row[4]},adcer={row[5]},dhlad={row[6]}, \
#hhlad={row[10]},pdg={row[7]},avyr={row[8]},ndg={row[11]}')
    #else:
        #pass
    zaznam = Record(number_in_row = iterator, datetime = index, pci1=row[0], pci2=row[1],pci=row[3],adtur=row[4],adcer=row[5],dhlad=row[6], \
                    hhlad=row[10],pdg=row[7],avyr=row[8],ndg=row[11])
    records.append(zaznam)
for i in range(0,len(records)-6):
    if records[i+1].ndg == records[i].ndg and \
    records[i+2].ndg == records[i].ndg and \
    records[i+3].ndg == records[i].ndg and \
    records[i+4].ndg == records[i].ndg and \
    records[i+5].ndg == records[i].ndg and \
    records[i].ndg < 0 and \
    records[i].pci1 > -325 and records[i].pci1 < -290 or \
    records[i].pci2 > -325 and records[i].pci2 < -290:
        best_rec.append(records[i])
        
for i in best_rec:
    #print(f' id {i.datetime} pci {i.pci} ndg = {i.ndg} hhlad = {i.hhlad}')
    pass
    
eff = {}
dolni_hladina = {}
cinny_vykon_1_stroje = {}    

for i in range(0,len(best_rec)-6):
    dt_i = datetime.strptime(best_rec[i].datetime.strip("'"),'%Y-%m-%d %H:%M')
    dt_ip1 = datetime.strptime(best_rec[i+1].datetime.strip("'"),'%Y-%m-%d %H:%M')
    d =dt_ip1-dt_i
    if d.total_seconds()==600:
        v_davyr = -best_rec[i].avyr + best_rec[i+1].avyr
        
        v_dadtur = -best_rec[i].adtur + best_rec[i+1].adtur
        v_ucinnost = abs(v_dadtur/v_davyr)
        v_dhlad =(best_rec[i].dhlad + best_rec[i+1].dhlad)/2
        v_adtur = best_rec[i].adtur
        v_pci = best_rec[i].pci/best_rec[i].ndg
        print(f'v_davyr{v_davyr}, v_dadtur{v_dadtur}, v_ucinnost{v_ucinnost},v_dhlad{v_dhlad},v_adtur{v_adtur},v_pci{v_pci}')
        #(dhlad.iloc[i][0]+dhlad.iloc[i-6][0])/2
        
        if v_dadtur != 0 and v_davyr != 0:
            eff[float(v_dhlad)] = float(abs(v_dadtur/v_davyr))
        print(f'pocet vzorku pro vypocet ucinnosti je {len(eff)}')
        dolni_hladina[v_adtur] = v_dhlad
        cinny_vykon_1_stroje[v_dhlad] = v_pci

breakpoint()
ucinnost = P.Polynomial.fit( [i for i in eff.keys()], [i for i in eff.values()],2)
dhladina = P.Polynomial.fit( [i for i in dolni_hladina.keys()], [i for i in dolni_hladina.values()],2)
vykon = P.Polynomial.fit( [i for i in cinny_vykon_1_stroje.keys()], [i for i in cinny_vykon_1_stroje.values()],2)

xx = np.linspace(min(eff.keys()), max(eff.keys()))
adt = np.linspace(min(dolni_hladina.keys()), max(dolni_hladina.keys()))
fig, ax1 = plt.subplots()
fig, ax2 = plt.subplots()
fig, ax3 = plt.subplots()

ax1.plot(xx, ucinnost(xx),c = 'red', label = ' ucinnost = f (DHlad)', linewidth=3)
ax1.scatter((eff.keys()) , (eff.values()))
ax2.plot(xx, vykon(xx),c = 'red', label = ' Pci = f (DHlad)', linewidth=3)
ax2.scatter((cinny_vykon_1_stroje.keys()) , (cinny_vykon_1_stroje.values()))
ax3.plot(adt, dhladina(adt),c = 'green', label = ' DHlad = f (ADtur)', linewidth=3)
ax3.scatter((dolni_hladina.keys()) , (dolni_hladina.values()))

legend = ax1.legend(loc='best', shadow=True, fontsize='small')
legend = ax2.legend(loc='best', shadow=True, fontsize='small')
legend = ax3.legend(loc='best', shadow=True, fontsize='small')
plt.show()
 #   
##v_davyr=(avyr.iloc[i-1][0]-avyr.iloc[i-5][0])
##                                    v_dadtur=(adtur.iloc[i-1][0]-adtur.iloc[i-5][0])
##                                    v_ucinnost = abs(v_dadtur/v_davyr)
##                                    if v_ucinnost > 0.9 or v_ucinnost < 0.7:
##                                        print(f'v_ucinnost je mimo : {v_ucinnost}')
##                                       
##                                        pass
##
##
##                                    v_dhlad = (dhlad.iloc[i][0]+dhlad.iloc[i-6][0])/2
##                                    v_adtur = adtur.iloc[i-3][0]
##                                    v_pci = (pci.iloc[i-3][0]/ndg.iloc[i-3][0])
##                                    if v_dadtur != 0 and v_davyr != 0:
##                                        eff[float(v_dhlad)] = float(abs(v_dadtur/v_davyr))
##                                    dolni_hladina[v_adtur] = v_dhlad
##                                    cinny_vykon_1_stroje[v_dhlad] = v_pci    
    
