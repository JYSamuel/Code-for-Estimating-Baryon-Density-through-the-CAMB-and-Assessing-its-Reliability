# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 22:54:34 2023

@author: WORK
"""

from matplotlib import pyplot as plt
import numpy as np


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


CAMB = CAMBdata('0.02235')
TTData = PlanckTTData()['bestfit']
TEData = PlanckTEData()['bestfit']
CAMBTT = CAMB['TT']
CAMBTE = CAMB['TE']
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
ls = np.arange(2, 500*5, 5)  
ls2 = np.arange(len(CAMBTT))
le = np.arange(2, 399*5, 5)
le2 = np.arange(len(CAMBTE))
Temptemp = TTData[:len(ls)] 
Tempol = TEData[:len(le)]
ax[0].plot(ls, Temptemp, label='Planck')
ax[0].plot(ls2, CAMBTT, label='CAMB')
ax[0].legend()
ax[0].plot()
ax[0].set_title(r'$TT\, [\mu K^2]$')
ax[0].set_xlim([2, 2500])
ax[0].set_ylim([0, 6100])
ax[0].set_xlabel(r'$\ell$')
ax[1].plot(le, Tempol, label='Planck')
ax[1].plot(le2, CAMBTE, label='CAMB')
ax[1].legend()
ax[1].plot()
ax[1].set_title(r'$TE\, [\mu K^2]$')
ax[1].set_xlim([2,2000])
ax[1].set_ylim([-160, 160])
ax[1].set_xlabel(r'$\ell$')

plt.show()


