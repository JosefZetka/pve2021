import numpy as np
from scipy import interpolate
from numpy import polynomial as P
import pdb
import grafy_eda
print(f' Spusten vypocet poctu hodin CP pro EDA na zaklade ADtur v MWh, pockej nez se objevi zavislosti potrebne pro vypocet.')
vysledek = grafy_eda.main()
vykon = vysledek[2]
dhladina = vysledek[1]
ucinnost  = vysledek [0]
#


#breakpoint()
#adtur = 2050
print("Zadej pro EDA ADtur:")
adtur = int(input())
adturmax = 2231-94

pocethodin = 0
dhmin = 290.8
pci_1 = 105
delta_dh =0# 0.26
print(f' minimalni dolni hladina = {dhmin}, predpokladany cinny vykon pro posledni hodinu CP = {pci_1}, delta zmenay DHlad za 1.oh = {delta_dh}')
##if adtur > pc:
##       adtur = adtur - pc
##       pocethodin = pocethodin +1
##else:
print(f' adtur = {adtur}')

while adtur < adturmax:
        dh = dhladina(adtur)
        print(f' adtur = {round(adtur,2)}, dh = {round(dh,2)}, pocethodin = {pocethodin}, ucinnost = { round(ucinnost(dh),2)}, vykon = {round(vykon(dh),2)}')

        adtur = adtur + vykon(dh+delta_dh)* ucinnost(dh+delta_dh)
        pocethodin = pocethodin +1
print(f'adturmax = {adturmax}, adtur = {adtur}')
print(' ------------------------------------------------------------------------------------------------------------------')
print(f'Vysledny pocet hodin cp je {pocethodin-1} hodin a {round(60 +((adturmax-adtur)*60/pci_1),0)} minut')
print(' ------------------------------------------------------------------------------------------------------------------')

try:
    input("Press enter to continue")
except SyntaxError:
    pass


