# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 2014

@author: gabriel
"""

from .._in import get_in_params as g
from ..phot_analysis.local_diag_clean import rm_stars as rm_s


def nmemb_select(n_memb, memb_prob_avrg_sort):
    '''
    Algorithm to select which stars to use by the best fit funtcion.
    Will set the minimum probability value such that an equal number of
    stars are used in the best fit process, as the approximate number of
    members found when comparing the density of the cluster region with that
    of the field regions defined.
    '''
    red_memb_fit, red_memb_no_fit, red_plot_pars = memb_prob_avrg_sort, [], []

    # Check approximate number of true members obtained by the structural
    # analysis.
    if n_memb > 10:

        # Total number of stars in the cluster region.
        n_tot = len(memb_prob_avrg_sort)

        # If there are less stars in the cluster region than than n_memb stars,
        # use all stars in the cluster region.
        if n_memb >= n_tot:
            # Use all stars in the cluster region.
            indx, red_plot_pars = n_tot, [0.]
        else:
            # Use the first n_memb stars, ie: those stars with the highest
            # membership probability values.
            indx, red_plot_pars = n_memb, \
            [zip(*memb_prob_avrg_sort)[-1][n_memb]]

        red_memb_fit, red_memb_no_fit = memb_prob_avrg_sort[:indx], \
        memb_prob_avrg_sort[indx:]

    else:
        print ("  WARNING: less than 10 stars identified as true\n"
        "  cluster members. Using full list.")

    return red_memb_fit, red_memb_no_fit, red_plot_pars


def top_h(memb_prob_avrg_sort):
    '''
    Reject stars in the lower half of the membership probabilities list.
    '''

    red_memb_fit, red_memb_no_fit, red_plot_pars = memb_prob_avrg_sort, [], []

    middle_indx = int(len(memb_prob_avrg_sort) / 2)
    red_fit = memb_prob_avrg_sort[:middle_indx]
    # Check number of stars left.
    if len(red_fit) > 10:
        red_memb_fit, red_memb_no_fit, red_plot_pars = red_fit, \
        memb_prob_avrg_sort[middle_indx:], \
        [memb_prob_avrg_sort[middle_indx][-1]]
    else:
        print ("  WARNING: less than 10 stars left after reducing\n"
        "  by top half membership probability. Using full list.")

    return red_memb_fit, red_memb_no_fit, red_plot_pars


def manual(memb_prob_avrg_sort, min_prob_man):
    '''
    Find index of star with membership probability < min_prob_man.
    '''

    red_memb_fit, red_memb_no_fit, red_plot_pars = memb_prob_avrg_sort, [], []

    indx = 0
    for star in memb_prob_avrg_sort:
        if star[-1] < min_prob_man:
            break
        else:
            indx += 1

    if len(memb_prob_avrg_sort[:indx]) > 10:
        red_memb_fit, red_memb_no_fit, red_plot_pars = \
        memb_prob_avrg_sort[:indx], memb_prob_avrg_sort[indx:],\
        [min_prob_man]
    else:
        print ("  WARNING: less than 10 stars left after reducing\n"
        "  by manual membership probability. Using full list.")

    return red_memb_fit, red_memb_no_fit, red_plot_pars


def man_mag(memb_prob_avrg_sort, min_prob_man):
    '''
    Reject stars beyond the given magnitude limit.
    '''

    red_memb_fit, red_memb_no_fit, red_plot_pars = memb_prob_avrg_sort, [], []

    red_fit, red_not_fit = [], []
    for star in memb_prob_avrg_sort:
        if star[3] <= min_prob_man:
            red_fit.append(star)
        else:
            red_not_fit.append(star)

    # Check number of stars left.
    if len(red_fit) > 10:
        red_memb_fit, red_memb_no_fit, red_plot_pars = red_fit, red_not_fit,\
        [min_prob_man]
    else:
        print ("  WARNING: less than 10 stars left after reducing\n"
        "  by magnitude limit. Using full list.")

    return red_memb_fit, red_memb_no_fit, red_plot_pars


def red_memb(n_memb, decont_algor_return, field_region):
    '''
    Reduce number of stars according to a given membership probability
    lower limit, minimum magnitude limit or local density-based removal.
    '''

    memb_prob_avrg_sort, flag_decont_skip = decont_algor_return
    mode_red_memb, local_bin, min_prob_man = g.rm_params

    # Default assignment.
    red_memb_fit, red_memb_no_fit, red_plot_pars = memb_prob_avrg_sort, [], []

    if mode_red_memb == 'skip':
        # Skip reduction process.
        print 'Reduced membership function skipped.'

    # If the DA was skipped and any method but 'local' is selected, don't run.
    elif flag_decont_skip and mode_red_memb != 'local':
        print ("  WARNING: decontamination algorithm was skipped.\n"
        "  Can't apply '{}' membership reduction method.\n"
        "  Using full list.").format(mode_red_memb)

    else:
        # This mode works even if the DA did not run.
        if mode_red_memb == 'local':
            red_memb_fit, red_memb_no_fit, red_plot_pars = \
            rm_s(decont_algor_return, field_region, local_bin)

        if mode_red_memb == 'n-memb':
            red_memb_fit, red_memb_no_fit, red_plot_pars = nmemb_select(n_memb,
                memb_prob_avrg_sort)

        elif mode_red_memb == 'top-h':
            red_memb_fit, red_memb_no_fit, red_plot_pars = \
            top_h(memb_prob_avrg_sort)

        elif mode_red_memb == 'man':
            red_memb_fit, red_memb_no_fit, red_plot_pars = \
            manual(memb_prob_avrg_sort, min_prob_man)

        elif mode_red_memb == 'mag':
            red_memb_fit, red_memb_no_fit, red_plot_pars = \
            man_mag(memb_prob_avrg_sort, min_prob_man)

        print 'Reduced membership function applied.'

    return red_memb_fit, red_memb_no_fit, red_plot_pars