# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 2014

@author: gabriel
"""


def red_memb(flag_area_stronger, decont_algor_return, rm_params):
    '''
    Reduce number of stars according to a given membership probability
    lower limit.
    '''

    memb_prob_avrg_sort, flag_decont_skip = decont_algor_return
    flag_red_memb, min_prob = rm_params

    skip_reduce = False
    if flag_red_memb in {'auto', 'manual'}:

        if flag_area_stronger is True:
            memb_prob_avrg_sort2 = memb_prob_avrg_sort
            print 'WARNING: no field regions found.'
            print "Can't apply membership reduction."
            skip_reduce = True

        if flag_decont_skip is True:
            print 'WARNING: decontamination algorithm skipped.'
            print "Can't apply membership reduction."
            skip_reduce = True

        if skip_reduce is not True:

            if flag_red_memb == 'auto':
                # Reject stars in the lower half of the membership
                # probabilities list.
                middle_indx = int(len(memb_prob_avrg_sort) / 2)
                memb_prob_avrg_sort2 = memb_prob_avrg_sort[:middle_indx]

            elif flag_red_memb == 'manual':

                memb_prob_avrg_sort2 = []
                for star in memb_prob_avrg_sort:
                    if star[7] >= min_prob:
                        memb_prob_avrg_sort2.append(star)
        else:
            # Skip reduction process.
            memb_prob_avrg_sort2 = memb_prob_avrg_sort
    else:
        # Skip reduction process.
        memb_prob_avrg_sort2 = memb_prob_avrg_sort

    return memb_prob_avrg_sort2