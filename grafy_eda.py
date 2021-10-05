import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from numpy import polynomial as P
import pdb

##SELECT convert(varchar(16),
##DATEADD(minute,1,MAX(DateTime)),120) as DateHour,
##ROUND(AVG(EPC2_Pci_f),0) as avg_EPC2_Pci_f,
##ROUND(AVG(EPC2_Pdg_f),0) as avg_EPC2_Pdg_f,
##ROUND(AVG(EPC2_Pci_21),0) as avg_EPC2_Pci_21,
##ROUND(AVG(EPC2_Pci_22),0) as avg_EPC2_Pci_22,
##ROUND(AVG(EPC2_Pci_20),0) as avg_EPC2_Pci_20,
##ROUND(MAX(EPC2_PlynSpotr_f),0) as max_EPC2_PlynSpotr,
##ROUND(MAX(EPC2_PlynSpotr24_f),0) as max_EPC2_PlynSpotr24,
##ROUND(AVG(EPC2_Pmaxtechbl_f),0) as avg_EPC2_Pmaxtechbl_f,
##ROUND(AVG(EPC2_T),0) as avg_EPC2_T
##FROM OpenQuery(INSQL,'SELECT dateTime,EPC2_Pci_f,EPC2_Pdg_f,EPC2_Pci_21,EPC2_Pci_22,EPC2_Pci_20,EPC2_PlynSpotr_f,EPC2_PlynSpotr24_f,EPC2_Pmaxtechbl_f,EPC2_T FROM Runtime.dbo.AnalogWideHistory WHERE DateTime>=''20210921 00:00:00'' AND DateTime<''20210922 00:00:00'' AND wwResolution=60000 AND wwRetrievalMode = ''cyclic'' and wwVersion = ''latest''')
##GROUP BY datePart(Year,DateTime),datePart(Month,DateTime),datePart(Day,DateTime),datePart(Hour,DateTime) Order by DateHour;

def main():
    p = r""  # bude brana z GUI
    #pci1=pd.read_excel( p  + 'HCP EDA_new.xls',index_col = [0],header =[0], skiprows = [0,1], usecols = [1,2])
    pci1=pd.read_csv( p  + 'eda.txt',index_col = [0], usecols = [0,1])
    
    pci2=pd.read_csv( p  + 'eda.txt',index_col = [0], usecols = [0,2])
    pci3=pd.read_csv( p  + 'eda.txt',index_col = [0], usecols = [0,3])
    pci4=pd.read_csv( p  + 'eda.txt',index_col = [0], usecols = [0,4])

    eda =  pd.read_csv( p  + 'eda.txt',index_col = [0], usecols = [0,7,9,10,11])
    #EDA_ADtur   EDA_DHlad  EDA_Pdg  EDA_Avyr_fs
    pci =  pd.read_csv( p  + 'eda.txt',index_col = [0],usecols = [0,6])
    #EDA_Pci_fs
    adtur =  pd.read_csv( p  + 'eda.txt',index_col = [0],usecols = [0,7])
    adcer =  pd.read_csv( p  + 'eda.txt',index_col = [0], usecols = [0,8])
    dhlad =  pd.read_csv( p  + 'eda.txt',index_col = [0], usecols = [0,9])
    pdg =  pd.read_csv( p  + 'eda.txt',index_col = [0], usecols = [0,10])
    avyr =  pd.read_csv( p  + 'eda.txt',index_col = [0], usecols = [0,11])
    ndg = pd.read_csv( p  + 'eda.txt',index_col = [0], usecols = [0,14])
    breakpoint()
    print(f' Pci  = {pci1}')
    e = 5
    tolerance = 20
    pcimin = -95

    eff = {}
    dolni_hladina = {}
    cinny_vykon_1_stroje = {}

    n = int(4)
    for i in range(6,len(eda),6):
        p = pci.iloc[i]
        pmax = pci.iloc[i][0]+e
        pmin = pci.iloc[i][0]-e
        if pci.iloc[i][0] > pmin and pci.iloc[i][0] < pmax and \
            pci.iloc[i-1][0] > pmin and pci.iloc[i-1][0] < pmax and \
                pci.iloc[i-2][0] > pmin and pci.iloc[i-2][0] < pmax and \
                    pci.iloc[i-3][0] > pmin and pci.iloc[i-3][0] < pmax and \
                        pci.iloc[i-4][0] > pmin and pci.iloc[i-4][0] < pmax and \
                            pci.iloc[i-5][0] > pmin and pci.iloc[i-5][0] < pmax and \
                                pci.iloc[i][0]*abs(ndg.iloc[i][0])<pcimin and \
                                    pci.iloc[i-1][0]*abs(ndg.iloc[i-1][0])<pcimin and \
                                        pci.iloc[i-2][0]*abs(ndg.iloc[i-2][0])<pcimin and \
                                            pci.iloc[i-3][0]*abs(ndg.iloc[i-3][0])<pcimin and \
                                                pci.iloc[i-4][0]*abs(ndg.iloc[i-4][0])<pcimin and \
                                                    pci.iloc[i-5][0]*abs(ndg.iloc[i-5][0])<pcimin and abs(ndg.iloc[i-3][0]) == n:
                                #print(f"pci je {pci.iloc[i][0]}")
                                if pci.iloc[i][0]< n* pcimin and pci.iloc[i][0]> n*(pcimin - tolerance):

                                    v_davyr=(avyr.iloc[i-1][0]-avyr.iloc[i-5][0])
                                    v_dadtur=(adtur.iloc[i-1][0]-adtur.iloc[i-5][0])
                                    v_ucinnost = abs(v_dadtur/v_davyr)
                                    if v_ucinnost > 0.9 or v_ucinnost < 0.7:
                                        print(f'v_ucinnost je mimo : {v_ucinnost}')
                                        # print(f'ucinnost = {v_ucinnost}')
                                        # print(f'pci.iloc[i-0][0] = {pci.iloc[i-0][0]}')
                                        # print(f'pci.iloc[i-1][0] = {pci.iloc[i-1][0]}')
                                        # print(f'pci.iloc[i-2][0] = {pci.iloc[i-2][0]}')
                                        # print(f'pci.iloc[i-3][0] = {pci.iloc[i-3][0]}')
                                        # print(f'pci.iloc[i-4][0] = {pci.iloc[i-4][0]}')
                                        # print(f'pci.iloc[i-5][0] = {pci.iloc[i-5][0]}')
                                        # print(f'pci.iloc[i-6][0] = {pci.iloc[i-6][0]}')

                                        # print(f'avyr.iloc[i-0][0] = {avyr.iloc[i-0][0]}')
                                        # print(f'avyr.iloc[i-1][0] = {avyr.iloc[i-1][0]}')
                                        # print(f'avyr.iloc[i-2][0] = {avyr.iloc[i-2][0]}')
                                        # print(f'avyr.iloc[i-3][0] = {avyr.iloc[i-3][0]}')
                                        # print(f'avyr.iloc[i-4][0] = {avyr.iloc[i-4][0]}')
                                        # print(f'avyr.iloc[i-5][0] = {avyr.iloc[i-5][0]}')
                                        # print(f'avyr.iloc[i-6][0] = {avyr.iloc[i-6][0]}')
                                        pass


                                    v_dhlad = (dhlad.iloc[i][0]+dhlad.iloc[i-6][0])/2
                                    v_adtur = adtur.iloc[i-3][0]
                                    v_pci = (pci.iloc[i-3][0]/ndg.iloc[i-3][0])
                                    if v_dadtur != 0 and v_davyr != 0:
                                        eff[float(v_dhlad)] = float(abs(v_dadtur/v_davyr))
                                    dolni_hladina[v_adtur] = v_dhlad
                                    cinny_vykon_1_stroje[v_dhlad] = v_pci


    #breakpoint()
    print(f'pocet vzorku pro vypocet ucinnosti je {len(eff)}')
    ucinnost = P.Polynomial.fit( [i for i in eff.keys()], [i for i in eff.values()],2)
    #ucinnost = interpolate.interp1d( [i for i in eff.keys()], [i for i in eff.values()],kind =1)
    
    
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
    return ucinnost, dhladina, vykon

if __name__ == "__main__" :
       main()
