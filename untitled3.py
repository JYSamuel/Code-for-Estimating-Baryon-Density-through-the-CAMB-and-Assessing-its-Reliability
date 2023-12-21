# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 04:58:24 2023

@author: WORK
"""

import os
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import savgol_filter

PTTdata_dict = {}
with open("COM_PowerSpect_CMB-TT-full_R3.01 (1).txt") as f:
    keys = f.readline().strip().split()[1:]
    PTTdata_dict = {key: [] for key in keys}
    for line in f:
       values = line.strip().split()
       for key, value in zip(keys, values):
            PTTdata_dict[key].append(float(value))

PTEdata_dict = {}
with open("COM_PowerSpect_CMB-TE-full_R3.01 (1).txt") as f:
    keys = f.readline().strip().split()[1:]
    PTEdata_dict = {key: [] for key in keys}
    for line in f:
       values = line.strip().split()
       for key, value in zip(keys, values):
            PTEdata_dict[key].append(float(value))


dataTT = PTTdata_dict['Dl']

dataTE = PTEdata_dict['Dl']

window_sizeTT = 65
poly_degreeTT = 3
window_sizeTE = 51
poly_degreeTE = 3

TTdownsampling_factor = len(dataTT) // 500
TEdownsampling_factor = len(dataTE) // 399

TTdownsampled_data = dataTT[::TTdownsampling_factor]
TEdownsampled_data = dataTE[::TEdownsampling_factor]

smoothed_TTdata = savgol_filter(TTdownsampled_data, window_sizeTT, poly_degreeTT)
smoothed_TEdata = savgol_filter(TEdownsampled_data, window_sizeTE, poly_degreeTE)

TTData = smoothed_TTdata
TEData = smoothed_TEdata
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
ls = np.arange(2, 500*5, 5) 
ls2 = np.arange(len(dataTT)) 
le = np.arange(2, 399*5, 5)
le2 = np.arange(len(dataTE))
Temptemp = TTData[:len(ls)] 
Tempol = TEData[:len(le)]
ax[0].plot(ls, Temptemp)
ax[0].scatter(ls2, dataTT, color='red')
ax[0].plot()
ax[0].set_title(r'$TT\, [\mu K^2]$')
ax[0].set_xlim([2, 2500])
ax[0].set_ylim([0, 6100])
ax[0].set_xlabel(r'$\ell$')
ax[1].plot(le, Tempol)
ax[1].scatter(le2, dataTE, color='red')
ax[1].plot()
ax[1].set_title(r'$TE\, [\mu K^2]$')
ax[1].set_xlim([2,2000])
ax[1].set_ylim([-160, 160])
ax[1].set_xlabel(r'$\ell$')

plt.show()




def GetNumbers(Data, bh):
    data_dict = Data
    output_folder = "ExtractedNumbers"
    output_file_name = f"{bh} output.txt"
    output_file_path = os.path.join(output_folder, output_file_name)
    with open(output_file_path, "w") as file:
        data = data_dict
        for value in data:
            file.write(str(value) + '\n')
            

GetNumbers(Temptemp, 'PlanckTT')
GetNumbers(Tempol, 'PlanckTE')