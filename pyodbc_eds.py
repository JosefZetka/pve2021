from datetime import datetime, timedelta
from time import gmtime, strftime
from CET_to_GMT import from_cet_to_gmt as converze
now = datetime.now()
import pyodbc
import pdb
import pyodbc 
server = '10.11.25.81' 
database = 'pvrData' 
username = 'pvruser' 
password = 'hQ2sGK+_TgtnBT4' 
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
cursor = cnxn.cursor()

variables = "dateTime,EDA_Pci_1,EDA_Pci_2,EDA_Pci_3,EDA_Pci_4,EDA_Pci_fq,EDA_Pci_fs,  EDA_ADtur, EDA_ADcer,EDA_DHlad, EDA_Pdg,EDA_Avyr_fs, EDA_Odtok,EDA_HHlad,EDA_Ndg_fs"

def vypocti(start_datettime, stop_datetime):

    dotaz = "SELECT convert(varchar(16),DATEADD(minute,1,MAX(DateTime)),120) as DateHour, \
    ROUND(AVG(EDS_Pci_1),0) as avg_EDS_Pci_1,     \
    ROUND(AVG(EDS_Pci_2),0) as avg_EDS_Pci_2,     \
    ROUND(AVG(EDS_Pci_fq),0) as avg_EDS_Pci_fq,     \
    ROUND(AVG(EDS_Pci_fs),0) as avg_EDS_Pci_fs,     \
    ROUND(AVG(EDS_ADtur),0) as avg_EDS_ADtur,     \
    ROUND(AVG(EDS_ADcer),0) as avg_EDS_ADcer,     \
    ROUND(AVG(EDS_DHlad),0) as avg_EDS_DHlad,     \
    ROUND(AVG(EDS_Pdg),0) as avg_EDS_Pdg,     \
    ROUND(AVG(EDS_Avyr_fs),0) as avg_EDS_Avyr_fs,     \
    ROUND(AVG(EDS_Odtok),0) as avg_EDS_Odtok,     \
    ROUND(AVG(EDS_HHlad),0) as avg_EDS_HHlad,     \
    ROUND(AVG(EDS_Ndg_fs),0) as avg_EDS_Ndg_fs      \
    FROM OpenQuery(INSQL,'SELECT dateTime,EDS_Pci_1,EDS_Pci_2,EDS_Pci_fq,EDS_Pci_fs,  EDS_ADtur, EDS_ADcer,EDS_DHlad, EDS_Pdg,EDS_Avyr_fs, EDS_Odtok,EDS_HHlad,EDS_Ndg_fs  \
    FROM Runtime.dbo.AnalogWideHistory     \
    WHERE DateTime>= ''" + start_datettime + "''  AND DateTime< ''" + stop_datetime + "''  AND wwResolution=60000 AND wwRetrievalMode = ''cyclic'' and wwVersion = ''latest''') \
    GROUP BY datePart(Year,DateTime),datePart(Month,DateTime),datePart(Day,DateTime),datePart(Hour,DateTime),datePart(Minute,DateTime)/10 Order by DateHour;"
    
##    dotaz = "SELECT convert(varchar(16),DATEADD(minute,1,MAX(DateTime)),120) as DateHour, \
##    ROUND(AVG(EDA_Pci_1),0) as avg_EDA_Pci_1, \
##    ROUND(AVG(EDA_Pci_2),0) as avg_EDA_Pci_2, \
##    ROUND(AVG(EDA_Pci_3),0) as avg_EDA_Pci_3, \
##    ROUND(AVG(EDA_Pci_4),0) as avg_EDA_Pci_4, \
##    ROUND(AVG(EDA_Pci_fq),0) as avg_EDA_Pci_fq, \
##    ROUND(AVG(EDA_Pci_fs),0) as avg_EDA_Pci_fs, \
##    ROUND(AVG(EDA_ADtur),0) as avg_EDA_ADtur, \
##    ROUND(AVG(EDA_ADcer),0) as avg_EDA_ADcer, \
##    ROUND(AVG(EDA_DHlad),0) as avg_EDA_DHlad, \
##    ROUND(AVG(EDA_Pdg),0) as avg_EDA_Pdg, \
##    ROUND(AVG(EDA_Avyr_fs),0) as avg_EDA_Avyr_fs, \
##    ROUND(AVG(EDA_Odtok),0) as avg_EDA_Odtok, \
##    ROUND(AVG(EDA_HHlad),0) as avg_EDA_HHlad, \
##    ROUND(AVG(EDA_Ndg_fs),0) as avg_EDA_Ndg_fs   \
##    FROM OpenQuery(INSQL,'SELECT dateTime,EDA_Pci_1,EDA_Pci_2,EDA_Pci_3,EDA_Pci_4,EDA_Pci_fq,EDA_Pci_fs,  EDA_ADtur, EDA_ADcer,EDA_DHlad, EDA_Pdg,EDA_Avyr_fs, EDA_Odtok,EDA_HHlad,EDA_Ndg_fs   \
##    FROM Runtime.dbo.AnalogWideHistory \
##    WHERE DateTime>= ''" + start_datettime + "''  AND DateTime< ''" + stop_datetime + "''  AND wwResolution=60000 AND wwRetrievalMode = ''cyclic'' and wwVersion = ''latest''') \
##    GROUP BY datePart(Year,DateTime),datePart(Month,DateTime),datePart(Day,DateTime),datePart(Hour,DateTime),datePart(Minute,DateTime)/10 Order by DateHour;"
    print(dotaz)
    cursor.execute(dotaz)
    #breakpoint()
    with open('eds.txt', 'w') as f:
        f.write("%s\n" % variables)
        for item in cursor:
    
            row = str(item)[1:-1]
            #breakpoint()
            f.write("%s\n" % row)

vypocti('20210901 00:00:00', '20211001 00:00:00')
    
##    print(f"dat {dat}")
##    for row in cursor:
##        print('row = %r' % (row,))
        
##for x in range(-1,0):
##  now = datetime.now() + timedelta(hours = x)
##  vypocti(now)
