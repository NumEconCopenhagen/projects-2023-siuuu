#%%
#Henter nødvendige pakker
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
from datetime import date, timedelta
from plotly.subplots import make_subplots
from unittest import skip
import chart_studio
import chart_studio.plotly as py
chart_studio.tools.set_credentials_file(username='MagnusBuggeArtha', api_key='bJBzJxYw7Jvxtf4EeEIf')

#Indhentning af historisk daglig kurshistorik + datahåndtering (BENYTTES IKKE LÆNGERE)
#DataNAV = pd.read_excel(r'X:\OpdateringsMappe\KursudviklingPræs_Data.xlsm', sheet_name="Data_NAV", usecols="A:F")
#DataNAV.to_excel(r'X:\OpdateringsMappe\Python Figurer\KurserHistorisk.xlsx', sheet_name="Data_NAV")
#DataNAV["Dato"] = pd.to_datetime(DataNAV["Dato"])
#DataNAV["DagNr"] = DataNAV["Dato"].dt.weekday
#DataNAV.drop(DataNAV.index[DataNAV['DagNr'] > 4], inplace=True)
#DataNAV = DataNAV.drop(columns = ["DagNr"], axis = 1)
#Today = date.today()
#DataNAV = DataNAV[DataNAV['Dato'] < dt.datetime.now()]
#DataNAV.to_excel(r'C:\Users\MagnusBugge\Artha Holding\Faelles - Documents\Medarbejdere\Magnus Bugge\Python\Kurser.xlsx', sheet_name="Data_NAV")

#Indhentning af data 2.0. KurserHistorisk stammer fra ovenstående kode samt indhentning af kurser fra Safe12Max

#Henter historisk data som er hentet fra Kursudvikling præs her findes en fil med gamle kurser
HistoriskNAVData = pd.read_excel(r'X:\OpdateringsMappe\Python Figurer\KurserHistorisk.xlsx', sheet_name="Data_NAV")
HistoriskNAVData.drop(HistoriskNAVData.columns[0], axis=1, inplace=True)
#Henter data fra Safe12Max derfor skal denne sørges for at være opdateret
DataSafe12Max = pd.read_excel(r'X:\OpdateringsMappe\Safe12Max.xlsm', sheet_name="Kurshistorik", usecols="B:G", skiprows=2)
DataSafe12Max = DataSafe12Max.rename(columns = {'DMax':'Dmax'})

#Fjerner data fra historisk udtræk som allerede indgår i Safe12Max
HistoriskNAVData = HistoriskNAVData[~HistoriskNAVData.Dato.isin(DataSafe12Max.Dato)]
HistoriskNAVData = HistoriskNAVData[HistoriskNAVData['Dato'] < '2021-12-31']

#Merger de to datasæt
dato_data = pd.DataFrame(pd.date_range(start='2012-10-01', end='today'), columns=['Dato'])

DataNAV = pd.merge(HistoriskNAVData, DataSafe12Max, how='outer', sort=True).fillna(method="ffill")
DataNAV = pd.merge(DataNAV, dato_data, how='outer', on='Dato', sort=True).fillna(method="ffill")

DataNAV.to_excel(r'X:\OpdateringsMappe\Python Figurer\DataNAV.xlsx', sheet_name="Data_NAV", index=False)


#Laver dataframe for hver fond og fjerner NA
Safe = DataNAV.drop(columns=['Optimum', 'Max', 'Responsible', 'Dmax']).dropna()
Optimum = DataNAV.drop(columns=['Safe', 'Max', 'Responsible', 'Dmax']).dropna()
Max = DataNAV.drop(columns=['Optimum', 'Safe', 'Responsible', 'Dmax']).dropna()
Responsible = DataNAV.drop(columns=['Optimum', 'Max', 'Safe', 'Dmax']).dropna()
Dmax = DataNAV.drop(columns=['Optimum', 'Max', 'Responsible', 'Safe']).dropna()

#Fjerner ens ved begyndelsen
Dmax = Dmax.iloc[5:]
Responsible = Responsible.iloc[7:]
Max = Max.iloc[17:]
Optimum = Optimum.iloc[6:]
Safe = Safe.iloc[17:]

Today = date.today()

#Fjerner blanks ift. datoer i fremtiden
DataNAV = DataNAV[DataNAV['Dato'] < datetime.datetime.now()]

#Laver liste med d. 30-12 i hvert år på nær seneste år, der er d. 31
FirstDateOfYear = ['2013-12-30', '2014-12-30', '2015-12-30', '2016-12-30',
               '2017-12-30', '2018-12-30', '2019-12-30', '2020-12-30',
               '2021-12-30', '2022-12-30', '2023-12-30', '2024-12-30',
               '2025-12-30', '2026-12-30', '2027-12-30', '2028-12-30']
FirstDateOfYear = pd.to_datetime(FirstDateOfYear)

#Laver ovenstående om til et dataframe
RebalanceringsDato = pd.DataFrame(FirstDateOfYear, columns = ['Dato'])

#Fjerner rebalanceringsdatoer i fremtiden
RebalanceringsDato = RebalanceringsDato.loc[(RebalanceringsDato['Dato'] < pd.to_datetime("today"))]

#Henter indeksdata indeholdende benchmarks
IndeksData = pd.read_excel(r'X:\MellemData\IndeksData.xlsm', sheet_name="Fonde", usecols="C,E, G:H, AB:AC, HM:HN, HQ:HR", skiprows=1)

#Splitter ovenstående og opdeler dem ift de respektive benchmarks
NykreditData = IndeksData.iloc[:, 0:2].dropna()
MSCIWorldData = IndeksData.iloc[:, 2:4].dropna()
CIBOR = IndeksData.iloc[:, 4:6].dropna()
EMSRIData = IndeksData.iloc[:, 6:8].dropna()
SRIData = IndeksData.iloc[:, 8:10].dropna()

#Renamer søjler
CIBOR = CIBOR.rename(columns = {CIBOR.columns[0]: 'Dato', CIBOR.columns[1]: 'CIBOR'})
NykreditData = NykreditData.rename(columns = {NykreditData.columns[0]: 'Dato', NykreditData.columns[1]: 'Nykredit'})
MSCIWorldData = MSCIWorldData.rename(columns = {MSCIWorldData.columns[0]: 'Dato', MSCIWorldData.columns[1]: 'MSCIWorld'})
SRIData = SRIData.rename(columns = {SRIData.columns[0]: 'Dato', SRIData.columns[1]: 'SRI'})
EMSRIData = EMSRIData.rename(columns = {EMSRIData.columns[0]: 'Dato', EMSRIData.columns[1]: 'EM SRI'})

SRIResponsible = pd.merge(Responsible, pd.merge(pd.merge(pd.merge(SRIData, EMSRIData, how='outer', on='Dato').fillna(method='ffill'), CIBOR, how='outer', on='Dato').fillna(method='ffill'), NykreditData, how='outer', on='Dato').fillna(method='ffill'), how='left', on='Dato').fillna(method='ffill')

#SRIResponsible.to_csv('test.csv', sep=';', decimal=',')

SRIResponsible["Responsible dagligt afkast"]=SRIResponsible["Responsible"].pct_change(1)
SRIResponsible["Nykredit dagligt afkast"]=SRIResponsible["Nykredit"].pct_change(1)
SRIResponsible["SRI dagligt afkast"]=SRIResponsible["SRI"].pct_change(1)
SRIResponsible["EM SRI dagligt afkast"]=SRIResponsible["EM SRI"].pct_change(1)

for ind, row in SRIResponsible.iterrows():
    if SRIResponsible.loc[ind, "Dato"] in FirstDateOfYear :
        SRIResponsible.loc[ind, "Løbende vægt Nykredit"] = 50 * (1 + SRIResponsible.loc[ind, "Nykredit dagligt afkast"])
        SRIResponsible.loc[ind, "Løbende vægt SRI"] = 44.25 * (1 + SRIResponsible.loc[ind, "SRI dagligt afkast"])
        SRIResponsible.loc[ind, "Løbende vægt EM SRI"] = 5.75 * (1 + SRIResponsible.loc[ind, "EM SRI dagligt afkast"])
        SRIResponsible.loc[ind, "Vægtsum"] = SRIResponsible.loc[ind, "Løbende vægt Nykredit"] + SRIResponsible.loc[ind, "Løbende vægt SRI"] + SRIResponsible.loc[ind, "Løbende vægt EM SRI"]
        SRIResponsible.loc[ind, "Ændring vægtsum"] = (SRIResponsible.loc[ind, "Vægtsum"]/100)-1
        SRIResponsible.loc[ind, "Indeks 100"] = SRIResponsible.loc[ind - 1, "Indeks 100"] * (1 + SRIResponsible.loc[ind, "Ændring vægtsum"])
    else :
        if ind == 0 :
            SRIResponsible.loc[ind, "Løbende vægt Nykredit"] = 50
            SRIResponsible.loc[ind, "Løbende vægt SRI"] = 44.25
            SRIResponsible.loc[ind, "Løbende vægt EM SRI"] = 5.75
            SRIResponsible.loc[ind, "Vægtsum"] = SRIResponsible.loc[ind, "Løbende vægt Nykredit"] + SRIResponsible.loc[ind, "Løbende vægt SRI"] + SRIResponsible.loc[ind, "Løbende vægt EM SRI"]
            SRIResponsible.loc[ind, "Ændring vægtsum"] = np.NaN
            SRIResponsible.loc[ind, "Indeks 100"] = 100
        else : 
            SRIResponsible.loc[ind, "Løbende vægt Nykredit"] = SRIResponsible.loc[ind-1, "Løbende vægt Nykredit"] * (1 + SRIResponsible.loc[ind, "Nykredit dagligt afkast"])
            SRIResponsible.loc[ind, "Løbende vægt SRI"] = SRIResponsible.loc[ind-1, "Løbende vægt SRI"] * (1 + SRIResponsible.loc[ind, "SRI dagligt afkast"])
            SRIResponsible.loc[ind, "Løbende vægt EM SRI"] = SRIResponsible.loc[ind-1, "Løbende vægt EM SRI"] * (1 + SRIResponsible.loc[ind, "EM SRI dagligt afkast"])
            SRIResponsible.loc[ind, "Vægtsum"] = SRIResponsible.loc[ind, "Løbende vægt Nykredit"] + SRIResponsible.loc[ind, "Løbende vægt SRI"] + SRIResponsible.loc[ind, "Løbende vægt EM SRI"]
            SRIResponsible.loc[ind, "Ændring vægtsum"] = (SRIResponsible.loc[ind, "Vægtsum"]/SRIResponsible.loc[ind-1, "Vægtsum"])-1
            SRIResponsible.loc[ind, "Indeks 100"] = SRIResponsible.loc[ind - 1, "Indeks 100"] * (1+ SRIResponsible.loc[ind, "Ændring vægtsum"])

#SRIResponsible.to_csv('test.csv', sep=';', decimal=',')

#Beregner indeks for Max
SRIResponsible["ResponsibleIndeks"] = (SRIResponsible["Responsible"]/SRIResponsible["Responsible"].iloc[0])*100

#Beregner standardafvigelse for Max og Benchmark
SRIResponsible["Responsible Std"]=SRIResponsible["Responsible dagligt afkast"].rolling(365).std()*(365**0.5)
SRIResponsible["Benchmark Std"]=SRIResponsible["Ændring vægtsum"].rolling(365).std()*(365**0.5)

#Merger Safe og Dmax med respektive relevante benchmarks, fylder tomme celler med ovenstående (hvis der ikke er data for benchmark benyttes tidligere observation)
NykreditSafe = pd.merge(Safe, NykreditData, how='left', on='Dato').fillna(method="ffill")
NykreditSafe = pd.merge(NykreditSafe, CIBOR, how='left', on='Dato').fillna(method="ffill")
NykreditSafe["NykreditIndeks"] = (NykreditSafe["Nykredit"]/NykreditSafe["Nykredit"].iloc[0])*100
NykreditSafe["SafeIndeks"] = (NykreditSafe["Safe"]/NykreditSafe["Safe"].iloc[0])*100
NykreditSafe["Safe dagligt afkast"] = NykreditSafe["Safe"].pct_change(1)
NykreditSafe["Nykredit dagligt afkast"] = NykreditSafe["Nykredit"].pct_change(1)
NykreditSafe["Safe Std"]=NykreditSafe["Safe dagligt afkast"].rolling(365).std()*(365**0.5)
NykreditSafe["Nykredit Std"]=NykreditSafe["Nykredit dagligt afkast"].rolling(365).std()*(365**0.5)

DMaxGlobaleAktier = pd.merge(Dmax, MSCIWorldData, how='left', on='Dato').fillna(method="ffill")
DMaxGlobaleAktier = pd.merge(DMaxGlobaleAktier, CIBOR, how='left', on='Dato').fillna(method="ffill")
DMaxGlobaleAktier["MSCIWorldIndeks"] = (DMaxGlobaleAktier["MSCIWorld"]/DMaxGlobaleAktier["MSCIWorld"].iloc[0])*100
DMaxGlobaleAktier["DmaxIndeks"] = (DMaxGlobaleAktier["Dmax"]/DMaxGlobaleAktier["Dmax"].iloc[0])*100
DMaxGlobaleAktier["Dmax dagligt afkast"] = DMaxGlobaleAktier["Dmax"].pct_change(1)
DMaxGlobaleAktier["MSCI World dagligt afkast"] = DMaxGlobaleAktier["MSCIWorld"].pct_change(1)
DMaxGlobaleAktier["Dmax Std"]=DMaxGlobaleAktier["Dmax dagligt afkast"].rolling(365).std()*(365**0.5)
DMaxGlobaleAktier["MSCI World Std"]=DMaxGlobaleAktier["MSCI World dagligt afkast"].rolling(365).std()*(365**0.5)

#Der benyttes kun data efter 2012-10-01 i præsentationsmaterialet, men data er større, irrelevant data fjernes.
Optimum = Optimum[Optimum['Dato'] >= '2012-09-01']
Max = Max[Max['Dato'] >= '2012-10-17']

#Danner benchmarkdata data, pba. indeks data for datoer der findes i begge hhv. nykredit og MSCI world data. Dernæst findes det data som også findes for artha .
BenchmarkMerge = pd.merge(NykreditData, MSCIWorldData, how='outer', on='Dato', sort=True).fillna(method="ffill")
BenchmarkMerge = pd.merge(BenchmarkMerge, CIBOR, how='outer', on='Dato', sort=True).fillna(method="ffill")

#Danner sammenligning ml optimum og 50-50 benchmark
FiftyFifty = pd.merge(Optimum, BenchmarkMerge, how='left', on='Dato', sort=True).fillna(method="ffill")
#Beregner daglige afkast for optimum og benchmarks
FiftyFifty["Optimum dagligt afkast"]=FiftyFifty["Optimum"].pct_change(1)
FiftyFifty["Nykredit dagligt afkast"]=FiftyFifty["Nykredit"].pct_change(1)
FiftyFifty["MSCI World dagligt afkast"]=FiftyFifty["MSCIWorld"].pct_change(1)

#Danner sammenligning ml max og 20-80 benchmark
TwentyEighty = pd.merge(Max, BenchmarkMerge, how='left', on='Dato', sort=True).fillna(method="ffill")

#Beregner daglige afkast for max og benchmarks
TwentyEighty["Max dagligt afkast"]=TwentyEighty["Max"].pct_change(1)
TwentyEighty["Nykredit dagligt afkast"]=TwentyEighty["Nykredit"].pct_change(1)
TwentyEighty["MSCI World dagligt afkast"]=TwentyEighty["MSCIWorld"].pct_change(1)

FiftyFifty = FiftyFifty[FiftyFifty['Dato'] >= '2012-09-30'].reset_index(drop=True)
TwentyEighty = TwentyEighty[TwentyEighty['Dato'] >= '2012-10-17'].reset_index(drop=True)

#Følgende iteration laver rebalancering for 20-80 benchmark ift. Max
for ind, row in TwentyEighty.iterrows():
    if TwentyEighty.loc[ind, "Dato"] in FirstDateOfYear :
        TwentyEighty.loc[ind, "Løbende vægt Nykredit"] = 20 * (1 + TwentyEighty.loc[ind, "Nykredit dagligt afkast"])
        TwentyEighty.loc[ind, "Løbende vægt MSCI World"] = 80 * (1 + TwentyEighty.loc[ind, "MSCI World dagligt afkast"])
        TwentyEighty.loc[ind, "Vægtsum"] = TwentyEighty.loc[ind, "Løbende vægt Nykredit"] + TwentyEighty.loc[ind, "Løbende vægt MSCI World"]
        TwentyEighty.loc[ind, "Ændring vægtsum"] = (TwentyEighty.loc[ind, "Vægtsum"]/100)-1
        TwentyEighty.loc[ind, "Indeks 100"] = TwentyEighty.loc[ind - 1, "Indeks 100"] * (1 + TwentyEighty.loc[ind, "Ændring vægtsum"])
    else :
        if ind == 0 :
            TwentyEighty.loc[ind, "Løbende vægt Nykredit"] = 20
            TwentyEighty.loc[ind, "Løbende vægt MSCI World"] = 80 
            TwentyEighty.loc[ind, "Vægtsum"] = TwentyEighty.loc[ind, "Løbende vægt Nykredit"] + TwentyEighty.loc[ind, "Løbende vægt MSCI World"]
            TwentyEighty.loc[ind, "Ændring vægtsum"] = np.NaN
            TwentyEighty.loc[ind, "Indeks 100"] = 100
        else : 
            TwentyEighty.loc[ind, "Løbende vægt Nykredit"] = TwentyEighty.loc[ind-1, "Løbende vægt Nykredit"] * (1 + TwentyEighty.loc[ind, "Nykredit dagligt afkast"])
            TwentyEighty.loc[ind, "Løbende vægt MSCI World"] = TwentyEighty.loc[ind-1, "Løbende vægt MSCI World"] * (1 + TwentyEighty.loc[ind, "MSCI World dagligt afkast"])
            TwentyEighty.loc[ind, "Vægtsum"] = TwentyEighty.loc[ind, "Løbende vægt Nykredit"] + TwentyEighty.loc[ind, "Løbende vægt MSCI World"]
            TwentyEighty.loc[ind, "Ændring vægtsum"] = (TwentyEighty.loc[ind, "Vægtsum"]/TwentyEighty.loc[ind-1, "Vægtsum"])-1
            TwentyEighty.loc[ind, "Indeks 100"] = TwentyEighty.loc[ind - 1, "Indeks 100"] * (1+ TwentyEighty.loc[ind, "Ændring vægtsum"])

#Fjerner irrelevante datoer
TwentyEighty = TwentyEighty[TwentyEighty['Dato'] <= MSCIWorldData["Dato"].iloc[-1]]

#Beregner indeks for Max
TwentyEighty["MaxIndeks"] = (TwentyEighty["Max"]/TwentyEighty["Max"].iloc[0])*100

#Beregner standardafvigelse for Max og Benchmark
TwentyEighty["Max Std"]=TwentyEighty["Max dagligt afkast"].rolling(365).std()*(365**0.5)
TwentyEighty["Benchmark Std"]=TwentyEighty["Ændring vægtsum"].rolling(365).std()*(365**0.5)

#Følgende iteration laver rebalancering for 50-50 benchmark ift. Optimum
for ind, row in FiftyFifty.iterrows():
    if FiftyFifty.loc[ind, "Dato"] in FirstDateOfYear :
        FiftyFifty.loc[ind, "Løbende vægt Nykredit"] = 50 * (1 + FiftyFifty.loc[ind, "Nykredit dagligt afkast"])
        FiftyFifty.loc[ind, "Løbende vægt MSCI World"] = 50 * (1 + FiftyFifty.loc[ind, "MSCI World dagligt afkast"])
        FiftyFifty.loc[ind, "Vægtsum"] = FiftyFifty.loc[ind, "Løbende vægt Nykredit"] + FiftyFifty.loc[ind, "Løbende vægt MSCI World"]
        FiftyFifty.loc[ind, "Ændring vægtsum"] = (FiftyFifty.loc[ind, "Vægtsum"]/100)-1
        FiftyFifty.loc[ind, "Indeks 100"] = FiftyFifty.loc[ind - 1, "Indeks 100"] * (1 + FiftyFifty.loc[ind, "Ændring vægtsum"])
    else :
        if ind == 0 :
            FiftyFifty.loc[ind, "Løbende vægt Nykredit"] = 50
            FiftyFifty.loc[ind, "Løbende vægt MSCI World"] = 50 
            FiftyFifty.loc[ind, "Vægtsum"] = FiftyFifty.loc[ind, "Løbende vægt Nykredit"] + FiftyFifty.loc[ind, "Løbende vægt MSCI World"]
            FiftyFifty.loc[ind, "Ændring vægtsum"] = np.NaN
            FiftyFifty.loc[ind, "Indeks 100"] = 100
        else : 
            FiftyFifty.loc[ind, "Løbende vægt Nykredit"] = FiftyFifty.loc[ind-1, "Løbende vægt Nykredit"] * (1 + FiftyFifty.loc[ind, "Nykredit dagligt afkast"])
            FiftyFifty.loc[ind, "Løbende vægt MSCI World"] = FiftyFifty.loc[ind-1, "Løbende vægt MSCI World"] * (1 + FiftyFifty.loc[ind, "MSCI World dagligt afkast"])
            FiftyFifty.loc[ind, "Vægtsum"] = FiftyFifty.loc[ind, "Løbende vægt Nykredit"] + FiftyFifty.loc[ind, "Løbende vægt MSCI World"]
            FiftyFifty.loc[ind, "Ændring vægtsum"] = (FiftyFifty.loc[ind, "Vægtsum"]/FiftyFifty.loc[ind-1, "Vægtsum"])-1
            FiftyFifty.loc[ind, "Indeks 100"] = FiftyFifty.loc[ind - 1, "Indeks 100"] * (1+ FiftyFifty.loc[ind, "Ændring vægtsum"])

#Fjerner irrelevante datoer
FiftyFifty = FiftyFifty[FiftyFifty['Dato'] <= MSCIWorldData["Dato"].iloc[-1]]

#Beregner indeks for Optimum
FiftyFifty["OptimumIndeks"] = (FiftyFifty["Optimum"]/FiftyFifty["Optimum"].iloc[0])*100

#Beregner standardafvigelse for Optimum og Benchmark
FiftyFifty["Optimum Std"]=FiftyFifty["Optimum dagligt afkast"].rolling(365).std()*(365**0.5)
FiftyFifty["Benchmark Std"]=FiftyFifty["Ændring vægtsum"].rolling(365).std()*(365**0.5)

#Definerer måned og år for hver række
TwentyEighty['Maned'] = pd.to_datetime(TwentyEighty["Dato"]).dt.to_period('M')

#Fjerner duplicates og beholder sidste (får sidste observation for hver måned)
TwentyEightyFirst_Dec_30 = TwentyEighty[(TwentyEighty["Dato"].dt.month == 12) & (TwentyEighty["Dato"].dt.day == 30)]
TwentyEightyFirst = TwentyEighty.drop_duplicates(subset=["Maned"], keep='last', inplace=False, ignore_index=False)

#Beregner månedligt afkast for max, benchmark
TwentyEightyFirst["Max maned afkast"]=TwentyEightyFirst["Max"].pct_change()
TwentyEightyFirst["Benchmark maned afkast"]=TwentyEightyFirst["Indeks 100"].pct_change()

#Beregner månedlig CIBOR
TwentyEightyFirst["CIBOR"]=(TwentyEightyFirst["CIBOR"]/100)/12

#Beregner mer' afkast for benchmark og max
TwentyEightyFirst["Benchmark mer maned afkast"]=TwentyEightyFirst["Benchmark maned afkast"]-TwentyEightyFirst["CIBOR"]
TwentyEightyFirst["Max mer maned afkast"]=TwentyEightyFirst["Max maned afkast"]-TwentyEightyFirst["CIBOR"]

#Sætter første observation lig kursudvikling præs (beregnet på historisk data)
TwentyEightyFirst.iloc[0, TwentyEightyFirst.columns.get_loc('Max mer maned afkast')] = -0.45698/100
TwentyEightyFirst.iloc[0, TwentyEightyFirst.columns.get_loc('Benchmark mer maned afkast')] = -0.65/100
#OBS skal nedenstående skal kun benyttes hvis månedsskiftet ikke er indgået
TwentyEightyFirst = TwentyEightyFirst[:-1]

TwentyEightyFirst.iloc[0, TwentyEightyFirst.columns.get_loc('Max maned afkast')] = -0.4498168/100

#Beregner gns månedligt afkast for benchmark og max
MiddelAfkastBM2080=TwentyEightyFirst["Benchmark mer maned afkast"].mean()
MiddelAfkastMax2080=TwentyEightyFirst["Max mer maned afkast"].mean()

#Beregner standardafvigelse for benchmark og max
StdAfkastMax2080 = TwentyEightyFirst["Max maned afkast"].std(ddof=0)*(12**0.5)
StdAfkastBM2080 = TwentyEightyFirst["Benchmark maned afkast"].std(ddof=0)*(12**0.5)

#Beregner sharpe ratio for benchmark og max
SharpeMax2080=MiddelAfkastMax2080/TwentyEightyFirst["Max mer maned afkast"].std(ddof=0)*(12**0.5)
SharpeBM2080=MiddelAfkastBM2080/TwentyEightyFirst["Benchmark mer maned afkast"].std(ddof=0)*(12**0.5)

TwentyEightyFirst = pd.concat([TwentyEightyFirst_Dec_30, TwentyEightyFirst], axis=0).sort_values('Dato').reset_index(drop=True)

current_month = datetime.datetime.now().strftime("%B")
if current_month == 'January':
    month_value = -3
else:
    month_value = -2

#SKAL ÆNDRES TIL -2 I FEBRUAR
TwentyEightyFirstATD = TwentyEighty.resample('Y', on='Dato')['Dato'].agg(['last']).iat[month_value, 0] - timedelta(days=1)
MaxFirstATD = TwentyEighty[TwentyEighty['Dato'] == TwentyEightyFirstATD]
TwentyEightyFirstATD_31 = TwentyEighty.resample('Y', on='Dato')['Dato'].agg(['last']).iat[month_value, 0]
MaxFirstATD_31 = TwentyEighty[TwentyEighty['Dato'] == TwentyEightyFirstATD_31]

TwentyEightyFirst.to_csv('TwentyEightyFirst.csv', sep=';', decimal=',')

#Beregner afkast År-til-dato
AfkastATD2080Max = (TwentyEightyFirst.iloc[-1, TwentyEightyFirst.columns.get_loc('Max')]/MaxFirstATD_31.iloc[0, MaxFirstATD_31.columns.get_loc('Max')])-1
AfkastATD2080BM = (TwentyEightyFirst.iloc[-1, TwentyEightyFirst.columns.get_loc('Indeks 100')]/MaxFirstATD.iloc[0, MaxFirstATD.columns.get_loc('Indeks 100')])-1

#Beregner afkast for hele perioden
AfkastTotal2080Max = (TwentyEightyFirst.iloc[-1, TwentyEightyFirst.columns.get_loc('Max')]/TwentyEighty.iloc[0, TwentyEighty.columns.get_loc('Max')])-1
AfkastTotal2080BM = (TwentyEightyFirst.iloc[-1, TwentyEightyFirst.columns.get_loc('Indeks 100')]/100)-1
#Definerer måned og år for hver række
FiftyFifty['Maned'] = FiftyFifty["Dato"].dt.to_period('M')

#Fjerner duplicates og beholder sidste (får sidste observation for hver måned)
FiftyFiftyFirst_Dec_30 = FiftyFifty[((FiftyFifty["Dato"].dt.month == 12) & (FiftyFifty["Dato"].dt.day == 30))]
FiftyFiftyFirst = FiftyFifty.drop_duplicates(subset=["Maned"], keep='last', inplace=False, ignore_index=False)

#Beregner månedligt afkast for optimum, benchmark
FiftyFiftyFirst["Optimum maned afkast"]= FiftyFiftyFirst["Optimum"].pct_change(1)
FiftyFiftyFirst["Benchmark maned afkast"]= FiftyFiftyFirst["Indeks 100"].pct_change(1)

#Beregner månedlig CIBOR
FiftyFiftyFirst["CIBOR"]=(FiftyFiftyFirst["CIBOR"]/100)/12

#Beregner mer' afkast for benchmark og optimum
FiftyFiftyFirst["Benchmark mer maned afkast"]=FiftyFiftyFirst["Benchmark maned afkast"]-FiftyFiftyFirst["CIBOR"]
FiftyFiftyFirst["Optimum mer maned afkast"]=FiftyFiftyFirst["Optimum maned afkast"]-FiftyFiftyFirst["CIBOR"]

#Sætter første observation lig kursudvikling præs (beregnet på historisk data)
FiftyFiftyFirst.iloc[0, FiftyFiftyFirst.columns.get_loc('Optimum mer maned afkast')] = -0.006226/100
FiftyFiftyFirst.iloc[0, FiftyFiftyFirst.columns.get_loc('Benchmark mer maned afkast')] = -0.65/100

#OBS skal nedenstående skal kun benyttes hvis månedsskiftet ikke er indgået
FiftyFiftyFirst = FiftyFiftyFirst[:-1]

FiftyFiftyFirst = FiftyFiftyFirst[1:]

#Beregner gns månedligt afkast for benchmark og optimum
MiddelAfkastBM5050=FiftyFiftyFirst["Benchmark mer maned afkast"].mean()
MiddelAfkastOptimum5050=FiftyFiftyFirst["Optimum mer maned afkast"].mean()

#Beregner standardafvigelse for benchmark og optimum
StdAfkastOptimum5050=FiftyFiftyFirst["Optimum mer maned afkast"].std()*(12**0.5)
StdAfkastBM5050 = FiftyFiftyFirst["Benchmark mer maned afkast"].std()*(12**0.5)

#Beregner sharpe ratio for benchmark og optimum
SharpeOptimum5050=(MiddelAfkastOptimum5050/FiftyFiftyFirst["Optimum mer maned afkast"].std())*(12**0.5)
SharpeBM5050=(MiddelAfkastBM5050/FiftyFiftyFirst["Benchmark mer maned afkast"].std())*(12**0.5)

FiftyFiftyFirst = pd.concat([FiftyFiftyFirst_Dec_30, FiftyFiftyFirst], axis=0).sort_values('Dato').reset_index(drop=True)

#SKAL ÆNDRES TIL -2 I FEBRUAR
FiftyFiftyFirstATD = FiftyFifty.resample('Y', on='Dato')['Dato'].agg(['last']).iat[month_value, 0] - timedelta(days=1)
OptimumFirstATD = FiftyFifty[FiftyFifty['Dato'] == FiftyFiftyFirstATD]
FiftyFiftyFirstATD_31 = FiftyFifty.resample('Y', on='Dato')['Dato'].agg(['last']).iat[month_value, 0]
OptimumFirstATD_31 = FiftyFifty[FiftyFifty['Dato'] == FiftyFiftyFirstATD_31]

FiftyFiftyFirst.to_csv('FiftyFiftyFirst.csv', sep=';', decimal=',')

#Beregner afkast År-til-dato
AfkastATD5050Optimum = (FiftyFiftyFirst.iloc[-1, FiftyFiftyFirst.columns.get_loc('Optimum')]/OptimumFirstATD_31.iloc[0, OptimumFirstATD_31.columns.get_loc('Optimum')])-1
AfkastATD5050BM = (FiftyFiftyFirst.iloc[-1, FiftyFiftyFirst.columns.get_loc('Indeks 100')]/OptimumFirstATD.iloc[0, OptimumFirstATD.columns.get_loc('Indeks 100')])-1

#Beregner afkast for hele perioden
AfkastTotal5050Optimum = (FiftyFiftyFirst.iloc[-1, FiftyFiftyFirst.columns.get_loc('Optimum')]/FiftyFifty.iloc[0, FiftyFifty.columns.get_loc('Optimum')])-1
AfkastTotal5050BM = (FiftyFiftyFirst.iloc[-1, FiftyFiftyFirst.columns.get_loc('Indeks 100')]/100)-1

#Definerer måned og år for hver række
SRIResponsible['Maned'] = SRIResponsible["Dato"].dt.to_period('M')

#Fjerner duplicates og beholder sidste (får sidste observation for hver måned)
SRIResponsibleFirst_Dec_30 = SRIResponsible[(SRIResponsible["Dato"].dt.month == 12) & (SRIResponsible["Dato"].dt.day == 30)]
SRIResponsibleFirst = SRIResponsible.drop_duplicates(subset=["Maned"], keep='last', inplace=False, ignore_index=False)
SRIResponsibleFirst = pd.concat([SRIResponsible[0:1], SRIResponsibleFirst])

#Beregner månedligt afkast for resp, benchmark
SRIResponsibleFirst["Responsible maned afkast"]=SRIResponsibleFirst["Responsible"].pct_change(1)
SRIResponsibleFirst["Benchmark maned afkast"]=SRIResponsibleFirst["Indeks 100"].pct_change(1)

#Beregner månedlig CIBOR
SRIResponsibleFirst["CIBOR"]=(SRIResponsibleFirst["CIBOR"]/100)/12

#Beregner mer' afkast for benchmark og optimum
SRIResponsibleFirst["Benchmark mer maned afkast"]=SRIResponsibleFirst["Benchmark maned afkast"]-SRIResponsibleFirst["CIBOR"]
SRIResponsibleFirst["Responsible mer maned afkast"]=SRIResponsibleFirst["Responsible maned afkast"]-SRIResponsibleFirst["CIBOR"]

#OBS skal nedenstående skal kun benyttes hvis månedsskiftet er indgået
SRIResponsibleFirst = SRIResponsibleFirst[:-1]

#Beregner gns månedligt afkast for benchmark og optimum
MiddelAfkastBMResp=SRIResponsibleFirst["Benchmark mer maned afkast"].mean()
MiddelAfkastResp=SRIResponsibleFirst["Responsible mer maned afkast"].mean()

#Beregner standardafvigelse for benchmark og optimum
StdAfkastResp=SRIResponsibleFirst["Responsible mer maned afkast"].std()*(12**0.5)
StdAfkastBMResp = SRIResponsibleFirst["Benchmark mer maned afkast"].std()*(12**0.5)

#Beregner sharpe ratio for benchmark og optimum
SharpeResponsible=(MiddelAfkastResp/SRIResponsibleFirst["Responsible mer maned afkast"].std())*(12**0.5)
SharpeBMResp=(MiddelAfkastBMResp/SRIResponsibleFirst["Benchmark mer maned afkast"].std())*(12**0.5)

SRIResponsibleFirst = pd.concat([SRIResponsibleFirst_Dec_30, SRIResponsibleFirst], axis=0).sort_values('Dato').reset_index(drop=True)

#SKAL ÆNDRES TIL -2 I FEBRUAR
SRIResponsibleFirstATD = SRIResponsible.resample('Y', on='Dato')['Dato'].agg(['last']).iat[month_value, 0] - timedelta(days=1)
ResponsibleFirstATD = SRIResponsible[SRIResponsible['Dato'] == SRIResponsibleFirstATD]
SRIResponsibleFirstATD_31 = SRIResponsible.resample('Y', on='Dato')['Dato'].agg(['last']).iat[month_value, 0]
ResponsibleFirstATD_31 = SRIResponsible[SRIResponsible['Dato'] == SRIResponsibleFirstATD_31]

SRIResponsibleFirst.to_csv('SRIResponsibleFirst.csv', sep=';', decimal=',')

#Beregner afkast År-til-dato
AfkastATDResp = (SRIResponsibleFirst.iloc[-1, SRIResponsibleFirst.columns.get_loc('Responsible')]/ResponsibleFirstATD_31.iloc[0, ResponsibleFirstATD_31.columns.get_loc('Responsible')])-1
AfkastATDBMResp = (SRIResponsibleFirst.iloc[-1, SRIResponsibleFirst.columns.get_loc('Indeks 100')]/ResponsibleFirstATD.iloc[0, ResponsibleFirstATD.columns.get_loc('Indeks 100')])-1

#Beregner afkast for hele perioden
AfkastTotalResp = (SRIResponsibleFirst.iloc[-1, SRIResponsibleFirst.columns.get_loc('Responsible')]/SRIResponsible.iloc[0, SRIResponsible.columns.get_loc('Responsible')])-1
AfkastTotalBMResp = (SRIResponsibleFirst.iloc[-1, SRIResponsibleFirst.columns.get_loc('Indeks 100')]/100)-1

#Definerer måned og år for hver række
NykreditSafe['Maned'] = NykreditSafe["Dato"].dt.to_period('M')

#Fjerner duplicates og beholder sidste (får sidste observation for hver måned)
NykreditSafeFirst_Dec_30 = NykreditSafe[((NykreditSafe["Dato"].dt.month == 12) & (NykreditSafe["Dato"].dt.day == 30))]
NykreditSafeFirst = NykreditSafe.drop_duplicates(subset=["Maned"], keep='last', inplace=False, ignore_index=False)

NykreditSafeFirst = pd.concat([NykreditSafe[0:1], NykreditSafeFirst])

#Beregner månedligt afkast for optimum, benchmark
NykreditSafeFirst["Safe maned afkast"]=NykreditSafeFirst["Safe"].pct_change(1)
NykreditSafeFirst["Benchmark maned afkast"]=NykreditSafeFirst["NykreditIndeks"].pct_change(1)

#Beregner månedlig CIBOR
NykreditSafeFirst["CIBOR"]=(NykreditSafeFirst["CIBOR"]/100)/12

#Beregner mer' afkast for benchmark og optimum
NykreditSafeFirst["Benchmark mer maned afkast"]=NykreditSafeFirst["Benchmark maned afkast"]-NykreditSafeFirst["CIBOR"]
NykreditSafeFirst["Safe mer maned afkast"]=NykreditSafeFirst["Safe maned afkast"]-NykreditSafeFirst["CIBOR"]

#OBS skal nedenstående skal kun benyttes hvis månedsskiftet ikke er indgået
NykreditSafeFirst = NykreditSafeFirst[:-1]

#Beregner gns månedligt afkast for benchmark og optimum
MiddelAfkastBMSafe=NykreditSafeFirst["Benchmark mer maned afkast"].mean()
MiddelAfkastSafe=NykreditSafeFirst["Safe mer maned afkast"].mean()

#Beregner standardafvigelse for benchmark og optimum
StdAfkastSafe=NykreditSafeFirst["Safe mer maned afkast"].std()*(12**0.5)
StdAfkastBMSafe = NykreditSafeFirst["Benchmark mer maned afkast"].std()*(12**0.5)

#Beregner sharpe ratio for benchmark og optimum
SharpeSafe=(MiddelAfkastSafe/NykreditSafeFirst["Safe mer maned afkast"].std())*(12**0.5)
SharpeBMSafe=(MiddelAfkastBMSafe/NykreditSafeFirst["Benchmark mer maned afkast"].std())*(12**0.5)

NykreditSafeFirst = pd.concat([NykreditSafeFirst_Dec_30, NykreditSafeFirst], axis=0).sort_values('Dato').reset_index(drop=True)

#SKAL ÆNDRES TIL -2 I FEBRUAR
NykreditSafeFirstATD = NykreditSafe.resample('Y', on='Dato')['Dato'].agg(['last']).iat[month_value, 0] - timedelta(days=1)
SafeFirstATD = NykreditSafe[NykreditSafe['Dato'] == NykreditSafeFirstATD]
NykreditSafeFirstATD_31 = NykreditSafe.resample('Y', on='Dato')['Dato'].agg(['last']).iat[month_value, 0]
SafeFirstATD_31 = NykreditSafe[NykreditSafe['Dato'] == NykreditSafeFirstATD_31]

NykreditSafeFirst.to_csv('NykreditSafeFirst.csv', sep=';', decimal=',')

#Beregner afkast År-til-dato
AfkastATDSafe = (NykreditSafeFirst.iloc[-1, NykreditSafeFirst.columns.get_loc('Safe')]/SafeFirstATD_31.iloc[0, SafeFirstATD_31.columns.get_loc('Safe')])-1
AfkastATDBMSafe = (NykreditSafeFirst.iloc[-1, NykreditSafeFirst.columns.get_loc('NykreditIndeks')]/SafeFirstATD.iloc[0, SafeFirstATD.columns.get_loc('NykreditIndeks')])-1

#Beregner afkast for hele perioden
AfkastTotalSafe = (NykreditSafeFirst.iloc[-1, NykreditSafeFirst.columns.get_loc('Safe')]/NykreditSafe.iloc[0, NykreditSafe.columns.get_loc('Safe')])-1
AfkastTotalBMSafe = (NykreditSafeFirst.iloc[-1, NykreditSafeFirst.columns.get_loc('NykreditIndeks')]/100)-1

#Definerer måned og år for hver række
DMaxGlobaleAktier['Maned'] = DMaxGlobaleAktier["Dato"].dt.to_period('M')

#Fjerner duplicates og beholder sidste (får sidste observation for hver måned)
DMaxGlobaleAktierFirst_Dec_30 = DMaxGlobaleAktier[((DMaxGlobaleAktier["Dato"].dt.month == 12) & (DMaxGlobaleAktier["Dato"].dt.day == 30))]
DMaxGlobaleAktierFirst = DMaxGlobaleAktier.drop_duplicates(subset=["Maned"], keep='last', inplace=False, ignore_index=False)

DMaxGlobaleAktierFirst = pd.concat([DMaxGlobaleAktier[0:1], DMaxGlobaleAktierFirst])

#Beregner månedligt afkast for optimum, benchmark
DMaxGlobaleAktierFirst["Dmax maned afkast"]=DMaxGlobaleAktierFirst["Dmax"].pct_change(1)
DMaxGlobaleAktierFirst["Benchmark maned afkast"]=DMaxGlobaleAktierFirst["MSCIWorldIndeks"].pct_change(1)

#Beregner månedlig CIBOR
DMaxGlobaleAktierFirst["CIBOR"]=(DMaxGlobaleAktierFirst["CIBOR"]/100)/12

#Beregner mer' afkast for benchmark og optimum
DMaxGlobaleAktierFirst["Benchmark mer maned afkast"]=DMaxGlobaleAktierFirst["Benchmark maned afkast"]-DMaxGlobaleAktierFirst["CIBOR"]
DMaxGlobaleAktierFirst["Dmax mer maned afkast"]=DMaxGlobaleAktierFirst["Dmax maned afkast"]-DMaxGlobaleAktierFirst["CIBOR"]

#OBS skal nedenstående skal kun benyttes hvis månedsskiftet ikke er indgået
DMaxGlobaleAktierFirst = DMaxGlobaleAktierFirst[:-1]

#Beregner gns månedligt afkast for benchmark og optimum
MiddelAfkastBMDmax=DMaxGlobaleAktierFirst["Benchmark mer maned afkast"].mean()
MiddelAfkastDmax=DMaxGlobaleAktierFirst["Dmax mer maned afkast"].mean()

#Beregner standardafvigelse for benchmark og optimum
StdAfkastDmax=DMaxGlobaleAktierFirst["Dmax mer maned afkast"].std()*(12**0.5)
StdAfkastBMDmax = DMaxGlobaleAktierFirst["Benchmark mer maned afkast"].std()*(12**0.5)

#Beregner sharpe ratio for benchmark og optimum
SharpeDmax=(MiddelAfkastDmax/DMaxGlobaleAktierFirst["Dmax mer maned afkast"].std())*(12**0.5)
SharpeBMDmax=(MiddelAfkastBMDmax/DMaxGlobaleAktierFirst["Benchmark mer maned afkast"].std())*(12**0.5)

DMaxGlobaleAktierFirst = pd.concat([DMaxGlobaleAktierFirst_Dec_30, DMaxGlobaleAktierFirst], axis=0).sort_values('Dato').reset_index(drop=True)


#SKAL ÆNDRES TIL -2 I FEBRUAR
DMaxGlobaleAktierFirstATD = DMaxGlobaleAktier.resample('Y', on='Dato')['Dato'].agg(['last']).iat[month_value, 0] - timedelta(days=1)
DmaxFirstATD = DMaxGlobaleAktier[DMaxGlobaleAktier['Dato'] == DMaxGlobaleAktierFirstATD]
DMaxGlobaleAktierFirstATD_31 = DMaxGlobaleAktier.resample('Y', on='Dato')['Dato'].agg(['last']).iat[month_value, 0]
DmaxFirstATD_31 = DMaxGlobaleAktier[DMaxGlobaleAktier['Dato'] == DMaxGlobaleAktierFirstATD_31]

DMaxGlobaleAktierFirst.to_csv('DMaxGlobaleAktierFirst.csv', sep=';', decimal=',')

#Beregner afkast År-til-dato
AfkastATDDmax = (DMaxGlobaleAktierFirst.iloc[-1, DMaxGlobaleAktierFirst.columns.get_loc('Dmax')]/DmaxFirstATD_31.iloc[0, DmaxFirstATD_31.columns.get_loc('Dmax')])-1
AfkastATDBMDmax = (DMaxGlobaleAktierFirst.iloc[-1, DMaxGlobaleAktierFirst.columns.get_loc('MSCIWorldIndeks')]/DmaxFirstATD.iloc[0, DmaxFirstATD.columns.get_loc('MSCIWorldIndeks')])-1

#Beregner afkast for hele perioden
AfkastTotalDmax = (DMaxGlobaleAktierFirst.iloc[-1, DMaxGlobaleAktierFirst.columns.get_loc('Dmax')]/DMaxGlobaleAktier.iloc[0, DMaxGlobaleAktier.columns.get_loc('Dmax')])-1
AfkastTotalBMDmax = (DMaxGlobaleAktierFirst.iloc[-1, DMaxGlobaleAktierFirst.columns.get_loc('MSCIWorldIndeks')]/100)-1

def kurserplot(FigurNavn, DatoSoejle, ArthaFond, FondsNavn, BMFond, BMNavn, StdFond, StdBM):
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=DatoSoejle, y=ArthaFond, mode='lines', line_color='#AD9E74', line_width=1.5, name=FondsNavn, fill= 'tozeroy', fillcolor='rgba(173, 158, 116, 0.05)'))
    fig.add_trace(go.Scatter(x=DatoSoejle, y=BMFond, mode='lines', line_color='#131D2F', line_width=1.5, name=BMNavn, fill= 'tozeroy', fillcolor='rgba(173, 158, 116, 0.05)'))
    fig.update_xaxes(title_text='', showgrid=False)

    ymax = max([ArthaFond.max(), BMFond.max()]) + 10
    ymin = min([ArthaFond.min(), BMFond.min()]) - 10

    fig.update_yaxes(title_text='', range=[ymin, ymax], gridcolor="#F0F0F0")

    fig.update_layout(
    plot_bgcolor="white",
    font_color="black",
    title=dict(text = "Afkast periode: " + DatoSoejle.iloc[365].strftime("%d-%m-%Y") + " til " + DatoSoejle.iloc[-1].strftime("%d-%m-%Y"), font=dict(size=16)),
    xaxis_range=[DatoSoejle.iloc[0], DatoSoejle.iloc[-1]],
    margin=dict(t=30,l=0,b=10,r=10),
    width=600,
    height=450,
    #xaxis=dict(tickformat="%Y"),
    font_family="Grandview",
    font = dict(
        size = 16
    ),
    legend=dict(
    orientation="h"
    )
    )
    fig.show()
    fig.write_image(fr"X:\OpdateringsMappe\Python Figurer\{FigurNavn}.png", scale=10)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=DatoSoejle, y=StdFond, mode='lines', line_color='#AD9E74',
                     line_width=1.5, name=FondsNavn, fill= 'tozeroy', fillcolor='rgba(173, 158, 116, 0.05)'))
    fig2.add_trace(go.Scatter(x=DatoSoejle, y=StdBM, mode='lines', line_color='#131D2F',
                     line_width=1.5, name=BMNavn, fill= 'tozeroy', fillcolor='rgba(173, 158, 116, 0.05)'))
    fig2.update_xaxes(title_text='', showgrid=False)
    fig2.update_yaxes(title_text='', gridcolor="#F0F0F0")
    fig2.update_layout(
        plot_bgcolor="white",
        font_color="black",
        #title=dict(text = "Risiko periode: " + str(DatoSoejle.iloc[365])[0:7] + " til " + (datetime.datetime.now() - datetime.timedelta(weeks=4)).strftime("%d-%m-%Y"), font=dict(size=16)),
        title=dict(text = "Risiko periode: " + DatoSoejle.iloc[365].strftime("%d-%m-%Y") + " til " + DatoSoejle.iloc[-1].strftime("%d-%m-%Y"), font=dict(size=16)),
        xaxis_range=[DatoSoejle.iloc[365], DatoSoejle.iloc[-1]],
        yaxis_tickformat = '.0%',margin=dict(t=30,l=0,b=10,r=10),
        #xaxis=dict(tickformat="%Y"),
        width=600,
        height=450,
        font_family="Grandview",
        font = dict(
            size = 16
        ),
        legend=dict(
        orientation="h"
    )
    )
    fig2.show()
    fig2.write_image(fr"X:\OpdateringsMappe\Python Figurer\{FigurNavn}Std.png", scale=10)

now = datetime.datetime.now().date()
eop = now.replace(day=1)
eop = str(eop)

NykreditSafe = NykreditSafe[NykreditSafe['Dato'] < eop]
FiftyFifty = FiftyFifty[FiftyFifty['Dato'] < eop]
TwentyEighty = TwentyEighty[TwentyEighty['Dato'] < eop]
DMaxGlobaleAktier = DMaxGlobaleAktier[DMaxGlobaleAktier['Dato'] < eop]
SRIResponsible = SRIResponsible[SRIResponsible['Dato'] < eop]

kurserplot("SafeGraf", NykreditSafe['Dato'], NykreditSafe['SafeIndeks'], "Artha Safe", NykreditSafe['NykreditIndeks'], "100% realkreditobl.", NykreditSafe["Safe Std"], NykreditSafe["Nykredit Std"])
kurserplot("OptimumGraf", FiftyFifty['Dato'], FiftyFifty['OptimumIndeks'], "Artha Optimum", FiftyFifty['Indeks 100'], "50/50% realkreditobl./globale aktier", FiftyFifty['Optimum Std'], FiftyFifty['Benchmark Std'])
kurserplot("MaxGraf", TwentyEighty["Dato"], TwentyEighty['MaxIndeks'], "Artha Max", TwentyEighty['Indeks 100'], "20/80% realkreditobl./globale aktier", TwentyEighty['Max Std'], TwentyEighty['Benchmark Std'])
kurserplot("DmaxGraf", DMaxGlobaleAktier['Dato'], DMaxGlobaleAktier['DmaxIndeks'], "Artha Dmax", DMaxGlobaleAktier['MSCIWorldIndeks'], "100% globale aktier", DMaxGlobaleAktier['Dmax Std'], DMaxGlobaleAktier['MSCI World Std'])
kurserplot("ResponsibleGraf", SRIResponsible['Dato'], SRIResponsible['ResponsibleIndeks'], "Artha Responsible", SRIResponsible['Indeks 100'], "50/50% realkreditobl./bæredygtige aktier", SRIResponsible['Responsible Std'], SRIResponsible['Benchmark Std'])

colors = ['white', 'white', '#F0F0F0']
data = {'Color' : colors}
df = pd.DataFrame(data)

ValuesOpti=[["Artha Optimum", "50/50% realkreditobl./globale aktier", "<b>Difference</b>"],
        ["{:.1%}".format(round(AfkastTotal5050Optimum,3)),"{:.1%}".format(round(AfkastTotal5050BM,3)), "{:.1%}".format(round(AfkastTotal5050Optimum-AfkastTotal5050BM,3))],
        ["{:.1%}".format(round(AfkastATD5050Optimum,3)), "{:.1%}".format(round(AfkastATD5050BM,3)),  "{:.1%}".format(round(AfkastATD5050Optimum-AfkastATD5050BM,3))],
        ["{:.1%}".format(round(StdAfkastOptimum5050,3)), "{:.1%}".format(round(StdAfkastBM5050,3)),  "{:.1%}".format(round(StdAfkastOptimum5050-StdAfkastBM5050,3))],
        ["{:.2f}".format(round(SharpeOptimum5050, 2)), "{:.2f}".format(round(SharpeBM5050, 2)), "{:.2f}".format(round(SharpeOptimum5050-SharpeBM5050, 2))]]

ValuesMax=[["Artha Max", "20/80% realkreditobl./globale aktier", "<b>Difference</b>"],
        ["{:.1%}".format(round(AfkastTotal2080Max,3)),"{:.1%}".format(round(AfkastTotal2080BM,3)), "{:.1%}".format(round(AfkastTotal2080Max-AfkastTotal2080BM,3))],
        ["{:.1%}".format(round(AfkastATD2080Max,3)), "{:.1%}".format(round(AfkastATD2080BM,3)),  "{:.1%}".format(round(AfkastATD2080Max-AfkastATD2080BM,3))],
        ["{:.1%}".format(round(StdAfkastMax2080,3)), "{:.1%}".format(round(StdAfkastBM2080,3)),  "{:.1%}".format(round(StdAfkastMax2080-StdAfkastBM2080,3))],
        ["{:.2f}".format(round(SharpeMax2080, 2)), "{:.2f}".format(round(SharpeBM2080, 2)), "{:.2f}".format(round(SharpeMax2080-SharpeBM2080, 2))]]

ValuesResp=[["Artha Responsible", "50/50% bæredygtige aktier/obl.", "<b>Difference</b>"],
        ["{:.1%}".format(round(AfkastTotalResp,3)),"{:.1%}".format(round(AfkastTotalBMResp,3)), "{:.1%}".format(round(AfkastTotalResp-AfkastTotalBMResp,3))],
        ["{:.1%}".format(round(AfkastATDResp,3)), "{:.1%}".format(AfkastATDBMResp),  "{:.1%}".format(round(AfkastATDResp-AfkastATDBMResp,3))],
        ["{:.1%}".format(round(StdAfkastResp,3)), "{:.1%}".format(round(StdAfkastBMResp,3)),  "{:.1%}".format(round(StdAfkastResp-StdAfkastBMResp,3))],
        ["{:.2f}".format(round(SharpeResponsible, 2)), "{:.2f}".format(round(SharpeBMResp, 2)), "{:.2f}".format(round(SharpeResponsible-SharpeBMResp, 2))]]

ValuesSafe=[["Artha Safe", "100% realkreditobl.", "<b>Difference</b>"],
        ["{:.1%}".format(round(AfkastTotalSafe,3)),"{:.1%}".format(round(AfkastTotalBMSafe,3)), "{:.1%}".format(round(AfkastTotalSafe-AfkastTotalBMSafe,3))],
        ["{:.1%}".format(round(AfkastATDSafe,3)), "{:.1%}".format(round(AfkastATDBMSafe,3)),  "{:.1%}".format(round(AfkastATDSafe-AfkastATDBMSafe,3))],
        ["{:.1%}".format(round(StdAfkastSafe,3)), "{:.1%}".format(round(StdAfkastBMSafe,3)),  "{:.1%}".format(round(StdAfkastSafe-StdAfkastBMSafe,3))],
        ["{:.2f}".format(round(SharpeSafe, 2)), "{:.2f}".format(round(SharpeBMSafe, 2)), "{:.2f}".format(round(SharpeSafe-SharpeBMSafe, 2))]]        

ValuesDmax=[["Artha Dmax", "100% globale aktier", "<b>Difference</b>"],
        ["{:.1%}".format(round(AfkastTotalDmax,3)),"{:.1%}".format(round(AfkastTotalBMDmax,3)), "{:.1%}".format(round(AfkastTotalDmax-AfkastTotalBMDmax,3))],
        ["{:.1%}".format(round(AfkastATDDmax,3)), "{:.1%}".format(round(AfkastATDBMDmax,3)),  "{:.1%}".format(round(AfkastATDDmax-AfkastATDBMDmax,3))],
        ["{:.1%}".format(round(StdAfkastDmax,3)), "{:.1%}".format(round(StdAfkastBMDmax,3)),  "{:.1%}".format(round(StdAfkastDmax-StdAfkastBMDmax,3))],
        ["{:.2f}".format(round(SharpeDmax, 2)), "{:.2f}".format(round(SharpeBMDmax, 2)), "{:.2f}".format(round(SharpeDmax-SharpeBMDmax, 2))]]        

def Table(FigurNavn, Values):
    Header=["<b>Afkast for periode</b>", "<b>Afkast siden start</b>", "<b>Afkast 2023</b>", "<b>Risiko</b>", "<b>Sharpe</b>"]
    TableFig = go.Figure(data=[go.Table(
        columnwidth = [310,160,120,80,80],
        header=dict(
        values=Header, 
        align=['left','center'],
        fill_color="white",
        font=dict(color='black', size=16)
        ),
        cells=dict(values=Values, 
        align=['left','center'],
        height=30,
        line_color=[df.Color],
        fill_color=[df.Color],
        font=dict(color='black', size=16)))])
    TableFig.show()
    TableFig.update_layout(width=700, height=150, margin={"l":0,"r":0,"t":0,"b":0}, font_family="Grandview")
    TableFig.write_image(fr"X:\OpdateringsMappe\Python Figurer\{FigurNavn}Table.png", scale=10)

Table("OptimumTest", ValuesOpti)
Table("MaxTest", ValuesMax)
Table("Responsible", ValuesResp)
Table("Safe", ValuesSafe)
Table("Dmax", ValuesDmax)


#%%
#%%
