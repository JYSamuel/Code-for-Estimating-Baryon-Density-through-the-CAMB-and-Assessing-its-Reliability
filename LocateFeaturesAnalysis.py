# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 00:51:28 2023

@author: WORK
"""


import numpy as np
from scipy.signal import find_peaks, peak_widths
from scipy.stats import chi2_contingency
import csv


def CAMBdata(bh):
    CAMBdata_dict = {'TT': [], 'TE': []}
    with open(f"ExtractedNumbers\{bh} output.txt") as f:
        for line in f:
            line = line.strip('[]')
            line = line.strip().strip(']')
            values = line.split()
            CAMBdata_dict['TT'].append(float(values[0]))
            CAMBdata_dict['TE'].append(float(values[3]))
    return CAMBdata_dict

def PlanckTTData():
    PTTdata_dict = {'bestfit':[]}
    with open("ExtractedNumbers\PlanckTT output.txt") as f:
        for line in f:
           values = line
           PTTdata_dict['bestfit'].append(float(values))
    return PTTdata_dict

def PlanckTEData():
    PTEdata_dict = {'bestfit':[]}
    with open("ExtractedNumbers\PlanckTE output.txt") as f:
        for line in f:
           values = line
           PTEdata_dict['bestfit'].append(float(values))
    return PTEdata_dict


def findPlanckTTParam(data):
    y = np.array(data['bestfit'])
    PlanckTTPOS, _ = find_peaks(y)
    PlanckTTAmp = y[PlanckTTPOS]
    PlanckTTWid, _, _, _ = peak_widths(y, PlanckTTPOS)
    psma_list = [PlanckTTAmp, PlanckTTPOS*5, PlanckTTWid*5]
    return(psma_list)
    
def findPlanckTEParam(data):
    y = np.array(data['bestfit'])
    PlanckTEPOS, _ = find_peaks(y)
    print(PlanckTEPOS)
    PlanckTEAmp = y[PlanckTEPOS]
    print(PlanckTEAmp)
    PlanckTEWid, _, _, _ = peak_widths(y, PlanckTEPOS)
    print(PlanckTEWid)
    invPy = -y
    invPlanckTEPOS, _ = find_peaks(invPy)
    invPlanckTEAmp = invPy[invPlanckTEPOS[0]]
    invPlanckTEWid, _, _, _ = peak_widths(invPy, invPlanckTEPOS)
    print(invPlanckTEAmp)
    print(invPlanckTEPOS)
    print(invPlanckTEWid)
    pall_list = [PlanckTEAmp, PlanckTEPOS*5, PlanckTEWid*5, invPlanckTEAmp, invPlanckTEPOS[0]*5, invPlanckTEWid[0]*5]
    return(pall_list)

def findCAMBParam(data):
    TTdata = np.array(data['TT'])
    TTpositions, _ = find_peaks(TTdata)
    TTamplitudes = TTdata[TTpositions[1:3]]
    TTwidths, _, _, _ = peak_widths(TTdata, TTpositions[1:3])
    TEdata = np.array(data['TE'])
    invTEdata = -TEdata
    TEpositions, _ = find_peaks(TEdata)
    TEamplitudes = TEdata[TEpositions[2:5]]
    TEwidths, _, _, _ = peak_widths(TEdata, TEpositions[2:5])
    TEantipos, _ = find_peaks(invTEdata)
    TEantiamp = invTEdata[TEantipos[1:2]]
    TEantiwid, _, _, _ = peak_widths(invTEdata, TEantipos[1:2])
    big_list = [TTpositions[1:3], TTamplitudes, TTwidths, TEpositions[2:5], TEamplitudes, TEwidths, TEantipos[1:2], TEantiamp, TEantiwid]
    return(big_list)

def createFile(): 
    SpectrumPara = ['Type', 'TT First Peak Position', 'TT Second Peak Position', 'TT First Peak Amplitude', 'TT Second Peak Amplitude', 'TT First Peak Width', 'TT Second Peak Width', 'TT 1,2 Amp Ratio', 'TE First Peak Position', 'TE Second Peak Position', 'TE Third Peak Position', 'TE First Antipeak Position', 'TE First Peak Amplitude', 'TE Second Peak Amplitude', 'TE Third Peak Amplitude', 'TE First Antipeak Amplitude', 'TE First Peak Width', 'TE Second Peak Width', 'TE Third Peak Width', 'TE First Antipeak Width', 'TE -1,2 Amp Ratio']
    PlanckTTP = [findPlanckTTParam(PlanckTTData())]
    PlanckTEP = [findPlanckTEParam(PlanckTEData())]
    rows = {'Type': ['Planck'], 'TT First Peak Position': [PlanckTTP[0][1][0]], 'TT Second Peak Position': [PlanckTTP[0][1][1]], 'TT First Peak Amplitude': [PlanckTTP[0][0][0]], 'TT Second Peak Amplitude': [PlanckTTP[0][0][1]], 'TT First Peak Width': [PlanckTTP[0][2][0]], 'TT Second Peak Width': [PlanckTTP[0][2][1]], 'TT 1,2 Amp Ratio': [PlanckTTP[0][0][0] / PlanckTTP[0][0][1]], 'TE First Peak Position': [PlanckTEP[0][1][1]], 'TE Second Peak Position': [PlanckTEP[0][1][2]], 'TE Third Peak Position': [PlanckTEP[0][1][3]], 'TE First Antipeak Position': [PlanckTEP[0][4]], 'TE First Peak Amplitude': [PlanckTEP[0][0][1]], 'TE Second Peak Amplitude': [PlanckTEP[0][0][2]], 'TE Third Peak Amplitude': [PlanckTEP[0][0][3]], 'TE First Antipeak Amplitude': [PlanckTEP[0][3]], 'TE First Peak Width': [PlanckTEP[0][2][1]], 'TE Second Peak Width': [PlanckTEP[0][2][2]], 'TE Third Peak Width': [PlanckTEP[0][2][3]], 'TE First Antipeak Width': [PlanckTEP[0][5]], 'TE -1,2 Amp Ratio': [PlanckTEP[0][3] / PlanckTEP[0][0][2]]}
    for x in np.arange(0.015, 0.03001, 0.00015):
        CAMBTTTEP = [findCAMBParam(CAMBdata(round(x, 5)))]
        rows['Type'].append('CAMB: ' + str(round(x, 5)))
        rows['TT First Peak Position'].append(CAMBTTTEP[0][0][0])
        rows['TT Second Peak Position'].append(CAMBTTTEP[0][0][1])
        rows['TT First Peak Amplitude'].append(CAMBTTTEP[0][1][0])
        rows['TT Second Peak Amplitude'].append(CAMBTTTEP[0][1][1])
        rows['TT First Peak Width'].append(CAMBTTTEP[0][2][0])
        rows['TT Second Peak Width'].append(CAMBTTTEP[0][2][1])
        rows['TT 1,2 Amp Ratio'].append(CAMBTTTEP[0][1][0]/CAMBTTTEP[0][1][1])
        rows['TE First Peak Position'].append(CAMBTTTEP[0][3][0])
        rows['TE Second Peak Position'].append(CAMBTTTEP[0][3][1])
        rows['TE Third Peak Position'].append(CAMBTTTEP[0][3][2])
        rows['TE First Antipeak Position'].append(CAMBTTTEP[0][6][0])
        rows['TE First Peak Amplitude'].append(CAMBTTTEP[0][4][0])
        rows['TE Second Peak Amplitude'].append(CAMBTTTEP[0][4][1])
        rows['TE Third Peak Amplitude'].append(CAMBTTTEP[0][4][2])
        rows['TE First Antipeak Amplitude'].append(CAMBTTTEP[0][7][0])
        rows['TE First Peak Width'].append(CAMBTTTEP[0][5][0])
        rows['TE Second Peak Width'].append(CAMBTTTEP[0][5][1])
        rows['TE Third Peak Width'].append(CAMBTTTEP[0][5][2])
        rows['TE First Antipeak Width'].append(CAMBTTTEP[0][8][0])
        rows['TE -1,2 Amp Ratio'].append(CAMBTTTEP[0][7][0]/CAMBTTTEP[0][4][1])
    with open('ResearchParameters2.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(SpectrumPara)
        writer.writerows(zip(*[rows[key] for key in SpectrumPara]))
    
    
def csv_to_dict_of_dicts():
    data_dict = {}

    with open('ResearchParameters2.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            key = row.pop('Type')  
            data_dict[key] = {param: value for param, value in row.items()}

    return data_dict
    
def perform_chi_square(data_dict):
    source_key = 'Planck'
    characteristics_dict = data_dict.get(source_key, {})
    expected_data = [float(value) for value in characteristics_dict.values()]
    data = {key: value for key, value in data_dict.items() if key != 'Planck'}
    chi_square_results = {}
    prob_value = {}
    print(expected_data)

    for dataset, values in data.items():
        observed_values = [float(value) for value in values.values()]
        print(observed_values)
        chi_square_statistic, P_value, _, _ = chi2_contingency([observed_values, expected_data])
        
        chi_square_results[dataset] = chi_square_statistic
        prob_value[dataset] = 1 - P_value
    
    print(chi_square_results)

    with open('Chi-squared.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Baryon Density', 'chi-square results', 'p-value']) 

        for key, value in chi_square_results.items():
            prob_value_for_key = prob_value.get(key, None)
            writer.writerow([key, value, prob_value_for_key])





def main():
    createFile()
    haha = csv_to_dict_of_dicts()
    print(haha)
    perform_chi_square(haha)




main()
