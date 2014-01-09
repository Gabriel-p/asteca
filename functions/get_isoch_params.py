# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 15:08:39 2014

@author: gabriel
"""

import os
from os.path import join

import numpy as np


def get_ranges_paths(sys_select):
    '''
    Reads parameters ranges and paths to stored isochrone files.
    '''
    
    # Girardi isochrones span a range of ~ 3.98+06 to 1.26e+10 yr.
    # MASSCLEAN clusters span a range of ~ 1.00e06 to 1.00e+10 yr.
    if sys_select == '1':
        # Range of values where the parameters will move.
        e_bv_min, e_bv_max, e_bv_step = 0., 1.01, 0.05
        dis_mod_min, dis_mod_max, dis_mod_step = 8., 13., 0.5
        z_min, z_max = 0.01, 0.03
        age_min, age_max = 0.003, 3.2
        
        # Path where isochrone files are stored.
        iso_path = '/media/rest/github/isochrones/iso_ubvi_marigo'
        
        # Data for files formatted for UBVI Marigo tracks.
        line_start = "#\tIsochrone\tZ = "
        mag_index = 9
         
    elif sys_select == '2':
        # Select cloud.
        cloud = raw_input('SMC or LMC cloud?')
        
        # Range of values where the parameters will move.
        e_bv_min, e_bv_max, e_bv_step = 0., 0.21, 0.01
        if cloud == 'SMC':
            dis_mod_min, dis_mod_max, dis_mod_step = 18.9, 18.91, 1
        elif cloud == 'LMC':
            dis_mod_min, dis_mod_max, dis_mod_step = 18.5, 18.51, 1
        z_min, z_max = 0.0005, 0.02
        age_min, age_max = 0.003, 12.6
    
        # Select Marigo or PARSEC tracks.        
        iso_select = raw_input('Select Marigo or PARSEC tracks as 1 or 2: ')
        if iso_select == '1':
            # Marigo.
            line_start = "#\tIsochrone\tZ = "
            mag_index = 9
            # Path where isochrone files are stored.
            iso_path = '/media/rest/github/isochrones/iso_wash_marigo'
        elif iso_select == '2':
            # PARSEC.
            line_start = "#\tIsochrone  Z = "
            mag_index = 10
            # Path where isochrone files are stored.
            iso_path = '/media/rest/github/isochrones/iso_wash_parsec'
    
    return e_bv_min, e_bv_max, e_bv_step, dis_mod_min, dis_mod_max,
    dis_mod_step, iso_path, line_start, mag_index
    
    

def move_track(sys_select, dis_mod, e_bv, iso_list, age_val):
    '''
    Recieves an isochrone of a given age and metallicity and modifies
    it according to given values for the extinction E(B-V) and distance
    modulus.
    '''
    iso_moved = [[], []]
    
    if sys_select == '1':
        # For UBVI system.
        #
        # E(B-V) = (B-V) - (B-V)o
        # Av = 3.1*E(B-V)
        # (mv - Mv)o = -5 + 5*log(d) + Av
        #
        Av = 3.1*e_bv
        for item in iso_list[age_val][1]:
            # mv affected by extinction.
            iso_moved[1].append(item + dis_mod + Av)
        for item in iso_list[age_val][0]:
            # (B-V) affected by extinction.
            iso_moved[0].append(item + e_bv)
    else:
        # For Washington system.
        #
        # E(C-T1) = 1.97*E(B-V) = (C-T1) - (C-T)o
        # M_T1 = T1 + 0.58*E(B-V) - (m-M)o - 3.2*E(B-V)
        #
        # (C-T1) = (C-T1)o + 1.97*E(B-V)
        # T1 = M_T1 - 0.58*E(B-V) + (m-M)o + 3.2*E(B-V)
        #
        V_Mv = dis_mod + 3.2*e_bv
        for item in iso_list[age_val][1]:
             # T1 magnitude affected by extinction.
            iso_moved[1].append(item - 0.58*e_bv + V_Mv)
        for item in iso_list[age_val][0]:
             # C-T1 color affected by extinction.
            iso_moved[0].append(item + 1.97*e_bv)    

    return iso_moved[0], iso_moved[1]    
    
    
    
def read_isochrones(sys_select):
    '''
    Reads and stores all isochrones available inside the indicated folder.
    '''

    # Call function to obtain these values.
    e_bv_min, e_bv_max, e_bv_step, dis_mod_min, dis_mod_max, dis_mod_step,\
    iso_path, line_start, mag_index = get_ranges_paths(sys_select)

    # This list will hold every isochrone of a given age, metallicity moved
    # according to given values of distance modulues and extinction.
    # Each isochrrone is stored as a list composed of two sub-lists, one for
    # the mag and one for the color:
    # funcs = [[[mag values],[color values]], [[],[]], ...]
    isochrones =[]
    # List that will hold all the ages, metallicities and extinctions associated
    # with the isochrone in the same indexed position in 'funcs'.
    # params = [[metal, age, E(B-V), dis_mod], [], ...]
    isoch_params = []
    # Iterate through all isochrone files.
    for iso_file in os.listdir(iso_path):
    
        # Read the entire file once to count the total number of ages in it.    
        with open(join(iso_path, iso_file), mode="r") as f_iso:
            ages_total = 0
            for line in f_iso:
                if line.startswith(line_start):
                    ages_total += 1
        
        # Open the isochrone for this cluster's metallicity.
        with open(join(iso_path, iso_file), mode="r") as f_iso:
            
            # Store metallicity value.
            if iso_file[:-4] == 'zams':
                metal = 0.019
            else:
                metal = float(iso_file[:-4])
        
            # List that will hold all the isochrones of the same metallicity.
            iso_list = [[[], []] for _ in \
                        range(len(os.listdir(iso_path))*ages_total)]
    
            # List that holds the ages in the isochrone file.
            ages = []
            # This var counts the number of ages within a given metallicity file.
            age_indx = -1
            # Iterate through each line in the file.
            for line in f_iso:
                
                if line.startswith(line_start):
                    age_indx += 1
                    # Store age value in 'ages' list.
                    for i, part in enumerate(line.split("Age =")):
                        # i=0 indicates the first part of that line, before 'Age ='
                        if i==1:
                            ages.append(float(part[:-3])/1.e09)
    
                # Save mag and color values for each isochrone.
                if not line.startswith("#"):
                    reader = line.split()
                    # Magnitude.
                    iso_list[age_indx][1].append(float(reader[mag_index]))
                    # Color.
                    iso_list[age_indx][0].append(float(reader[8]) -
                    float(reader[mag_index]))
    
            # Separate isochrones with different ages.
            for age_val in range(age_indx+1):
                
                # Move isochrone according to E(B-V) and dis_mod values thus
                # generating a new function. Store this function in
                # 'isochrones' list.
                for e_bv in np.arange(e_bv_min, e_bv_max, e_bv_step):
                    
                    for dis_mod in np.arange(dis_mod_min, dis_mod_max,
                                             dis_mod_step):
                        
                        # Store params for this isochrone.
                        isoch_params.append([metal, ages[age_val],
                                             round(e_bv, 2), round(dis_mod, 2)])
                        
                        # Call function to move track.
                        iso_moved_0, iso_moved_1 = move_track(sys_select, \
                        dis_mod, e_bv, iso_list, age_val) 
                        # Append final x and y CMD data to array.
                        isochrones.append([iso_moved_0, iso_moved_1])
                    
    return isochrones, isoch_params




def gip(memb_prob_avrg_sort):
    '''
    Main function.
    
    Perform a best fitting process to find the cluster's parameters:
    E(B-V), distance (distance modulus), age and metallicity.
    '''

    # Select photometric system to be used.
    sys_select = raw_input('Select UBVI or Washington system as 1 or 2: ')    
    
    
    return isoch_fit_params