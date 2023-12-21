# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 20:07:52 2023

@author: WORK
"""


import os
from matplotlib import pyplot as plt
import numpy as np
import camb
print('Using CAMB %s installed at %s'%(camb.__version__,os.path.dirname(camb.__file__)))

def paramSet(omega):
    pars = camb.CAMBparams()
    pars.set_cosmology(H0=67.5, ombh2=omega, omch2=0.122, mnu=0.06, omk=0, tau=0.06)
    pars.InitPower.set_params(As=2e-9, ns=0.965, r=0)
    pars.set_for_lmax(2500, lens_potential_accuracy=0);
    return pars

def calculation(mete):
    pars = mete
    results = camb.get_results(pars)
    powers =results.get_cmb_power_spectra(pars, CMB_unit='muK')
    for name in powers: print(name)
    return powers

def graphresults(ful, omega):
    powers = ful
    lensedTTL = powers['total']
    print(lensedTTL.shape)
    ls = np.arange(lensedTTL.shape[0])
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle(omega, fontsize=16)
    ax[0].plot(ls, lensedTTL[:, 0], color='C2', label='total')
    ax[0].set_title(r'$TT\, [\mu K^2]$')
    ax[0].legend()
    ax[0].set_xlim([2, 2500])
    ax[0].set_ylim([0, 6100])
    ax[1].plot(ls, lensedTTL[:, 3], color='C2', label='total')
    ax[1].set_title(r'$TE\, [\mu K^2]$')
    ax[1].legend()
    ax[1].set_xlim([2,2000])
    ax[1].set_ylim([-160, 160])
    for a in ax:  
        a.set_xlabel(r'$\ell$')
    GetNumbers(powers, omega)
    

def PlanckTTData():
    PTTdata_dict = {}
    with open("PlanckTTdata.txt") as f:
        keys = f.readline().strip().split()[1:]
        PTTdata_dict = {key: [] for key in keys}
        for line in f:
           values = line.strip().split()
           for key, value in zip(keys, values):
                PTTdata_dict[key].append(float(value))
    return PTTdata_dict

def PlanckTEData():
    PTEdata_dict = {}
    with open("PlanckTEdata.txt") as f:
        keys = f.readline().strip().split()[1:]
        PTEdata_dict = {key: [] for key in keys}
        for line in f:
           values = line.strip().split()
           for key, value in zip(keys, values):
                PTEdata_dict[key].append(float(value))
    return PTEdata_dict

def GraphPlanck(TT, TE):
    TTData = TT
    TEData = TE
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle('Planck Data', fontsize=16)
    ls = TTData['l']
    Temptemp = TTData['BestFit']
    ls2 = TEData['l']
    Temppola = TEData['BestFit']
    ax[0].plot(ls, Temptemp, color='m')
    ax[0].set_title(r'$TT\, [\mu K^2]$')
    ax[0].set_xlim([2, 2500])
    ax[0].set_ylim([0, 6100])
    ax[1].plot(ls2, Temppola, color='m')
    ax[1].set_title(r'$TE\, [\mu K^2]$')
    ax[1].set_xlim([2,2000])
    ax[1].set_ylim([-160, 160])
    for a in ax:  
        a.set_xlabel(r'$\ell$')

def GetNumbers(Data, bh):
    data_dict = Data
    output_folder = "ExtractedNumbers"
    output_file_name = f"{bh} output.txt"
    output_file_path = os.path.join(output_folder, output_file_name)
    with open(output_file_path, "w") as file:
        data = data_dict['total']
        for value in data:
            file.write(str(value) + '\n')

def main(): 
    TTdata = PlanckTTData()
    TEdata = PlanckTEData()
    GraphPlanck(TTdata, TEdata)
    for x in np.arange(0.015, 0.03001, 0.00015):
        pars = paramSet(round(x, 5))
        powers = calculation(pars)
        graphresults(powers, round(x, 5))

main()