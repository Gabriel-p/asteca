"""
@author: gabriel
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Rectangle
from matplotlib.ticker import MultipleLocator
from scipy.optimize import fsolve
from itertools import cycle
from scipy import stats
import matplotlib.mlab as mlab
from scipy.ndimage.filters import gaussian_filter
from matplotlib.patches import Ellipse
from os.path import join
import warnings


def make_plots(output_subdir, clust_name, x_data, y_data, center_params,
    rdp_params, backg_value, radius_params,
    cont_index, mag_data, col1_data, popt_mag, popt_col1,
    err_plot, rjct_errors_fit, k_prof, k_pr_err, d_b_k, flag_king_no_conver,
    stars_in, stars_out, stars_in_rjct, stars_out_rjct, integr_return, n_c,
    flag_area_stronger, cluster_region, field_region, pval_test_params,
    qq_params, memb_prob_avrg_sort, completeness, bf_params, bf_return,
    ga_params, er_params, axes_params, ps_params, pl_params):
    '''
    Make all plots.
    '''

    def star_size(x, a, c, area):
        '''
        function to obtain the optimal star size for the scatter plot.
        '''
        return sum(a * np.exp(x * mag_data ** c)) / area - 0.001

    def func(x, a, b, c):
        '''
        Exponential function.
        '''
        return a * np.exp(b * x) + c

    def line(x, slope, intercept):
        '''
        Linar function.
        '''
        y = slope * x + intercept
        return y

    def three_params(x):
        '''
        Three parameters King profile fit.
        '''
        a, b, c, d = k_prof[0], k_prof[1], k_prof[2], backg_value
        return c * (1 / np.sqrt(1 + (x / a) ** 2) - 1 /
        np.sqrt(1 + (b / a) ** 2)) ** 2 + d

    # Name for axes.
    x_ax, y_ax = axes_params[0], axes_params[1]

    # Define plot limits for *all* CMD diagrams.
    x_min_cmd, x_max_cmd, y_min_cmd, y_max_cmd = axes_params[2]
    col1_min, col1_max = max(x_min_cmd, min(col1_data) - 0.2),\
    min(x_max_cmd, max(col1_data) + 0.2)
    mag_min, mag_max = min(y_max_cmd, max(mag_data) + 0.5),\
    max(y_min_cmd, min(mag_data) - 0.5)

    # Unpack params.
    # Selected system params.
    sys_select = ps_params[1]
    m_rs, a_rs, e_rs, d_rs = ps_params[3:]
    # Parameters from get_center function.
    bin_list, h_filter, bin_center, centers_kde, cent_stats, kde_pl = \
    center_params[0], center_params[3], center_params[4], center_params[5], \
    center_params[6], center_params[7]
    center_cl = [center_params[5][0][0], center_params[5][0][1]]
    # RDP params.
    radii, ring_density, poisson_error = rdp_params
    # Parameters from get_radius function.
    clust_rad, delta_backg, delta_percentage = radius_params
    # Error parameters.
    be, be_e, e_max = er_params
    # Parameters from error fitting.
    bright_end, popt_umag, pol_mag, popt_ucol1, pol_col1, mag_val_left,\
    mag_val_right, col1_val_left, col1_val_right = err_plot
    # Integrated magnitude distribution.
    cl_reg_mag, fl_reg_mag, integ_mag, cl_reg_col, fl_reg_col, integ_col =\
    integr_return
    # Best isochrone fit params.
    bf_flag, best_fit_algor, N_b = bf_params
    # Genetic algorithm params.
    n_pop, n_gen, fdif, p_cross, cr_sel, p_mut, n_el, n_ei, n_es = ga_params
    # Best fitting process results.
    isoch_fit_params, isoch_fit_errors, shift_isoch, synth_clst = bf_return

    # Plot all outputs
    # figsize(x1, y1), GridSpec(y2, x2) --> To have square plots: x1/x2 =
    # y1/y2 = 2.5
    fig = plt.figure(figsize=(20, 35))  # create the top-level container
    gs1 = gridspec.GridSpec(14, 8)  # create a GridSpec object
    #gs1.update(wspace=.09, hspace=.0)

    # 2D not-weighted gaussian convolved histogram, smallest bin width.
    ax0 = plt.subplot(gs1[0:2, 0:2])
    plt.xlabel('x (bins)', fontsize=12)
    plt.ylabel('y (bins)', fontsize=12)
    ax0.minorticks_on()
    plt.axvline(x=bin_center[0], linestyle='--', color='white')
    plt.axhline(y=bin_center[1], linestyle='--', color='white')
    # Radius
    circle = plt.Circle((bin_center[0], bin_center[1]),
        clust_rad / bin_list[0], color='w', fill=False)
    fig.gca().add_artist(circle)
    # Add text boxs.
    text = 'Bin: %d px' % (bin_list[0])
    plt.text(0.05, 0.92, text, transform=ax0.transAxes,
             bbox=dict(facecolor='white', alpha=0.8), fontsize=12)
    text1 = '$x_{cent} = %d \pm %d px$' '\n' % (center_cl[0], bin_list[0])
    text2 = '$y_{cent} = %d \pm %d px$' % (center_cl[1], bin_list[0])
    text = text1 + text2
    plt.text(0.53, 0.85, text, transform=ax0.transAxes,
        bbox=dict(facecolor='white', alpha=0.85), fontsize=15)
    plt.imshow(h_filter.transpose(), origin='lower', aspect='auto')

    # 2D not-weighted histograms' centers.
    ax1 = plt.subplot(gs1[0:2, 2:4])
    # Get max and min values in x,y
    x_min, x_max = min(x_data), max(x_data)
    y_min, y_max = min(y_data), max(y_data)
    #Set plot limits
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xlabel('x (px)', fontsize=12)
    plt.ylabel('y (px)', fontsize=12)
    ax1.minorticks_on()
    # Add lines through meadian values with std deviations.
    plt.axvline(x=cent_stats[0][0], linestyle='-', color='k')
    plt.axvline(x=cent_stats[0][0] + cent_stats[1][0], linestyle='--',
        color='k')
    plt.axvline(x=cent_stats[0][0] - cent_stats[1][0], linestyle='--',
        color='k')
    plt.axhline(y=cent_stats[0][1], linestyle='-', color='k')
    plt.axhline(y=cent_stats[0][1] + cent_stats[1][1], linestyle='--',
        color='k')
    plt.axhline(y=cent_stats[0][1] - cent_stats[1][1], linestyle='--',
        color='k')
    # Add stats box.
    text1 = r'$(\tilde{x},\, \tilde{y}) = (%0.0f, %0.0f)\,px$' '\n' % \
    (cent_stats[0][0], cent_stats[0][1])
    text2 = '$(\sigma_x,\, \sigma_y) = (%0.0f, %0.0f)\,px$' % \
    (cent_stats[1][0], cent_stats[1][1])
    text = text1 + text2
    plt.text(0.05, 0.88, text, transform=ax1.transAxes,
        bbox=dict(facecolor='white', alpha=0.8), fontsize=11)
    cols = ['red', 'blue', 'green', 'black']
    for i in range(len(bin_list)):
        boxes = plt.gca()
        boxes.add_patch(Rectangle(((centers_kde[i][0] - bin_list[i]),
            (centers_kde[i][1] - bin_list[i])), bin_list[i] * 2.,
            bin_list[i] * 2., facecolor='none', edgecolor=cols[i], ls='solid',
            lw=1.5, zorder=(len(bin_list) - i),
            label='Bin: %d px' % bin_list[i]))
    # get handles
    handles, labels = ax1.get_legend_handles_labels()
    # use them in the legend
    leg1 = ax1.legend(handles, labels, loc='upper right', numpoints=1,
        fontsize=7)
    # Set the alpha value of the legend.
    leg1.get_frame().set_alpha(0.5)

    ## 2D weighted histogram's centers.
    #ax2 = plt.subplot(gs1[0:2, 4:6])
    ##Set plot limits
    #plt.xlim(x_min, x_max)
    #plt.ylim(y_min, y_max)
    #plt.xlabel('x (px)', fontsize=12)
    #plt.ylabel('y (px)', fontsize=12)
    #ax2.minorticks_on()
    ## Add lines through meadian values with std deviations.
    #plt.axvline(x=cent_stats[2][0], linestyle='-', color='k')
    #plt.axvline(x=cent_stats[2][0] + cent_stats[3][0], linestyle='--',
        #color='k')
    #plt.axvline(x=cent_stats[2][0] - cent_stats[3][0], linestyle='--',
        #color='k')
    #plt.axhline(y=cent_stats[2][1], linestyle='-', color='k')
    #plt.axhline(y=cent_stats[2][1] + cent_stats[3][1], linestyle='--',
        #color='k')
    #plt.axhline(y=cent_stats[2][1] - cent_stats[3][1], linestyle='--',
        #color='k')
    ## Add stats box.
    #text1 = r'$(\tilde{x},\, \tilde{y}) = (%0.0f, %0.0f)\,px$' '\n' % \
    #(cent_stats[2][0], cent_stats[2][1])
    #text2 = '$(\sigma_x,\, \sigma_y) = (%0.0f, %0.0f)\,px$' % \
    #(cent_stats[3][0], cent_stats[3][1])
    #text = text1 + text2
    #plt.text(0.05, 0.88, text, transform=ax2.transAxes,
        #bbox=dict(facecolor='white', alpha=0.85), fontsize=11)
    #cols = ['red', 'blue', 'green', 'black']
    #for i in range(len(bin_list)):
        #boxes = plt.gca()
        #boxes.add_patch(Rectangle(((center_coords[1][i][0] - bin_list[i] / 2.),
            #(center_coords[1][i][1] - bin_list[i] / 2.)), bin_list[i] * 2.,
            #bin_list[i] * 2., facecolor='none', edgecolor=cols[i], ls='solid',
            #lw=2., zorder=(len(bin_list) - i)))

    ## 2D weighted gaussian convolved histogram, smallest bin width.
    #ax3 = plt.subplot(gs1[0:2, 6:8])
    #plt.xlabel('x (bins)', fontsize=12)
    #plt.ylabel('y (bins)', fontsize=12)
    #ax3.minorticks_on()
    #plt.axvline(x=x_center_bin[1], linestyle='--', color='white')
    #plt.axhline(y=y_center_bin[1], linestyle='--', color='white')
    ## Add text boxs.
    #text1 = 'Bin: %d px' '\n' % (bin_list[0])
    #text2 = '(weighted)'
    #text = text1 + text2
    #plt.text(0.05, 0.87, text, transform=ax3.transAxes,
             #bbox=dict(facecolor='white', alpha=0.8), fontsize=12)
    #text1 = '$x_{cent} = %d \pm %d px$' '\n' % (center_coords[1][0][0],
        #bin_list[0])
    #text2 = '$y_{cent} = %d \pm %d px$' % (center_coords[1][0][1],
        #bin_list[0])
    #text = text1 + text2
    #plt.text(0.53, 0.85, text, transform=ax3.transAxes,
        #bbox=dict(facecolor='white', alpha=0.85), fontsize=15)
    #plt.imshow(h_filter[1].transpose(), origin='lower', aspect='auto')

    # x,y finding chart of full frame
    ax4 = plt.subplot(gs1[2:4, 0:2])
    #Set plot limits
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    #Set axis labels
    plt.xlabel('x (px)', fontsize=12)
    plt.ylabel('y (px)', fontsize=12)
    # Set minor ticks
    ax4.minorticks_on()
    # Plot r_cl.
    circle = plt.Circle((center_cl[0], center_cl[1]), clust_rad, color='r',
        fill=False, lw=2.5)
    fig.gca().add_artist(circle)
    # Plot r_t if K-P converged.
    if flag_king_no_conver is False:
        if k_prof[0] > 0:
            circle = plt.Circle((center_cl[0], center_cl[1]), k_prof[0],
                color='g', fill=False, ls='dashed', lw=2.5)
            fig.gca().add_artist(circle)
        # Plot tidal radius.
        circle = plt.Circle((center_cl[0], center_cl[1]), k_prof[1], color='g',
            fill=False, lw=2.5)
        fig.gca().add_artist(circle)
    # Add text box
    text1 = '$x_{cent} = %d \pm %d px$' '\n' % (center_cl[0], bin_list[0])
    text2 = '$y_{cent} = %d \pm %d px$' % (center_cl[1], bin_list[0])
    text = text1 + text2
    plt.text(0.53, 0.85, text, transform=ax4.transAxes,
        bbox=dict(facecolor='white', alpha=0.85), fontsize=15)
    # Plot stars.
    a, c = 200., 2.5
    area = (max(x_data) - min(x_data)) * (max(y_data) - min(y_data))
    # Solve for optimal star size.
    b = fsolve(star_size, backg_value, args=(a, c, area))
    plt.scatter(x_data, y_data, marker='o', c='black',
        s=a * np.exp(b * mag_data ** c))

    # Radial density plot.
    ax5 = plt.subplot(gs1[2:4, 2:6])
    # Get max and min values in x,y
    x_max = max(radii) + 10
    y_min, y_max = (backg_value - delta_backg) - (max(ring_density) -
    min(ring_density)) / 10, max(ring_density) + (max(ring_density) -
    min(ring_density)) / 10
    # Set plot limits
    plt.xlim(-10, x_max)
    plt.ylim(y_min, y_max)
    # Set axes labels
    plt.xlabel('radius (px)', fontsize=12)
    plt.ylabel("stars/px$^{2}$", fontsize=12)
    # Cluster's name.
    text = str(clust_name)
    plt.text(0.4, 0.9, text, transform=ax5.transAxes, fontsize=14)
    # Legend texts
    # Calculate errors for fitted King parameters. Use sqrt since the error
    # given by 'curve_fit' is the variance and we want the standard deviation.
    if flag_king_no_conver is False:
        rc_err = round(np.sqrt(k_pr_err[0][0]))
        rt_err = round(np.sqrt(k_pr_err[1][1]))
    else:
        rc_err, rt_err = -1, -1
    texts = ['RDP (%d px)' % bin_list[0],
            'backg = %.1E $st/px^{2}$' % backg_value,
            '$\Delta$=%d%%' % delta_percentage,
            '3-P King prof (%d px)' % d_b_k,
            'r$_c$ = %d $\pm$ %d px' % (k_prof[0], rc_err),
            'r$_t$ = %d $\pm$ %d px' % (k_prof[1], rt_err),
            'r$_{cl}$ = %d $\pm$ %d px' % (clust_rad, round(bin_list[0]))]
    # Plot density profile with the smallest bin size
    ax5.plot(radii, ring_density, 'ko-', zorder=3, label=texts[0])
    # Plot poisson error bars
    plt.errorbar(radii, ring_density, yerr=poisson_error, fmt='ko',
                 zorder=1)
    # Plot background level.
    ax5.hlines(y=backg_value, xmin=0, xmax=max(radii),
               label=texts[1], color='b', zorder=5)
    # Plot the delta around the background value used to asses when the density
    # has become stable
    plt.hlines(y=(backg_value + delta_backg), xmin=0, xmax=max(radii),
               color='b', linestyles='dashed', label=texts[2], zorder=2)
    # Approx middle of the graph.
    arr_y_up = (y_max - y_min) / 2.3 + y_min
    # Length of arrow head.
    #head_w = abs((arr_y_up - backg_value) / 10.)
    head_w, head_l = x_max * 0.023, (y_max - y_min) * 0.045
    # Length of arrow.
    arr_y_dwn = -1. * abs(arr_y_up - backg_value) * 0.76
    # Plot King profile.
    if flag_king_no_conver is False:
        ax5.plot(radii, three_params(radii), 'g--', label=texts[3],
                 lw=2., zorder=3)
        # Plot r_c as a dashed line.
        ax5.vlines(x=k_prof[0], ymin=0, ymax=three_params(k_prof[0]),
                   label=texts[4], color='g', linestyles=':', lw=4., zorder=4)
        # Plot r_t radius as an arrow. vline is there to show the label.
        ax5.vlines(x=k_prof[1], ymin=0., ymax=0., label=texts[5], color='g')
        ax5.arrow(k_prof[1], arr_y_up, 0., arr_y_dwn, fc="g", ec="g",
                  head_width=head_w, head_length=head_l, zorder=5)
    # Plot radius.
    ax5.vlines(x=clust_rad, ymin=0, ymax=0., label=texts[6], color='r')
    ax5.arrow(clust_rad, arr_y_up, 0., arr_y_dwn, fc="r",
              ec="r", head_width=head_w, head_length=head_l, zorder=5)
    # get handles
    handles, labels = ax5.get_legend_handles_labels()
    # use them in the legend
    ax5.legend(handles, labels, loc='upper right', numpoints=2, fontsize=12)
    ax5.minorticks_on()

    # Zoom on x,y finding chart
    ax6 = plt.subplot(gs1[2:4, 6:8])
    #Set plot limits
    x_min, x_max = min(x_data), max(x_data)
    y_min, y_max = min(y_data), max(y_data)
    # If possible, zoom in.
    x_min, x_max = max(x_min, (center_cl[0] - 1.5 * clust_rad)), \
    min(x_max, (center_cl[0] + 1.5 * clust_rad))
    y_min, y_max = max(y_min, (center_cl[1] - 1.5 * clust_rad)), \
    min(y_max, (center_cl[1] + 1.5 * clust_rad))
    # Prevent axis stretching.
    if (x_max - x_min) != (y_max - y_min):
        lst = [(x_max - x_min), (y_max - y_min)]
        val, idx = min((val, idx) for (idx, val) in enumerate(lst))
        if idx == 0:
            x_max = x_min + lst[1]
        else:
            y_max = y_min + lst[0]
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    #Set axis labels
    plt.xlabel('x (px)', fontsize=12)
    plt.ylabel('y (px)', fontsize=12)
    # Set minor ticks
    ax6.minorticks_on()
    # Add circle
    circle = plt.Circle((center_cl[0], center_cl[1]), clust_rad, color='r',
        fill=False, lw=1.5)
    fig.gca().add_artist(circle)
    text1 = 'Cluster (zoom)\n'
    text2 = 'CI = %0.2f' % (cont_index)
    text = text1 + text2
    plt.text(0.62, 0.9, text, transform=ax6.transAxes,
             bbox=dict(facecolor='white', alpha=0.85), fontsize=12)
    # Plor contour levels.
    # Get KDE for CMD intrinsic position of most probable members.
    #x, y = np.mgrid[x_min:x_max:100j, y_min:y_max:100j]
    #positions = np.vstack([x.ravel(), y.ravel()])
    #x_zoom, y_zoom = [], []
    #for indx, star_x in enumerate(x_data):
        #if x_min < star_x < x_max and y_min < y_data[indx] < y_max:
            #x_zoom.append(star_x)
            #y_zoom.append(y_data[indx])
    #values = np.vstack([x_zoom, y_zoom])
    ## The results are HEAVILY dependant on the bandwidth used here.
    #kernel = stats.gaussian_kde(values)

    #k_pos = kernel(positions)
    ## Print x,y coordinates of max value.
    #new_cent = positions.T[np.argmax(k_pos)]
    #print new_cent
    ext_range, x, y, k_pos = kde_pl
    kde = np.reshape(k_pos.T, x.shape)
    plt.imshow(np.rot90(kde), cmap=plt.cm.YlOrBr, extent=ext_range)
    plt.contour(x, y, kde, 10, colors='k', linewidths=0.6)
    # Plot stars.
    plt.scatter(x_data, y_data, marker='o', c='black',
        s=a * np.exp(b * mag_data ** c), zorder=4)
    #Plot center.
    plt.scatter(center_cl[0], center_cl[1], color='w', s=40, lw=0.8,
        marker='x', zorder=5)
    #plt.scatter(new_cent[0], new_cent[1], color='g', s=40, lw=0.8,
        #marker='x', zorder=5)

    # Cluster and field regions defined.
    ax7 = plt.subplot(gs1[4:6, 0:2])
    # Get max and min values in x,y
    x_min, x_max = min(x_data), max(x_data)
    y_min, y_max = min(y_data), max(y_data)
    #Set plot limits
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    #Set axis labels
    plt.xlabel('x (px)', fontsize=12)
    plt.ylabel('y (px)', fontsize=12)
    # Set minor ticks
    ax7.minorticks_on()
    ax7.grid(b=True, which='both', color='gray', linestyle='--', lw=0.5)
    # Radius
    circle = plt.Circle((center_cl[0], center_cl[1]), clust_rad,
                        color='r', fill=False)
    fig.gca().add_artist(circle)
    plt.text(0.4, 0.92, 'Cluster + %d Field regions' % (len(field_region)),
             transform=ax7.transAxes,
             bbox=dict(facecolor='white', alpha=0.8), fontsize=12)
    # Plot cluster region.
    clust_reg_temp = [[], []]
    for star in cluster_region:
        dist = np.sqrt((center_cl[0] - star[1]) ** 2 +
        (center_cl[1] - star[2]) ** 2)
        # Only plot stars inside the cluster's radius.
        if dist <= clust_rad:
            clust_reg_temp[0].append(star[1])
            clust_reg_temp[1].append(star[2])
    plt.scatter(clust_reg_temp[0], clust_reg_temp[1], marker='o', c='black',
                s=8, edgecolors='none')
    if not(flag_area_stronger):
        # Plot field stars regions.
        col = cycle(['red', 'darkgreen', 'blue', 'maroon'])
        for i, reg in enumerate(field_region):
            stars_reg_temp = [[], []]
            for star in reg:
                # star[1] is the x coordinate and star[2] the y coordinate
                stars_reg_temp[0].append(star[1])
                stars_reg_temp[1].append(star[2])
            plt.scatter(stars_reg_temp[0], stars_reg_temp[1], marker='o',
                        c=next(col), s=8, edgecolors='none')

    # Field stars CMD (stars outside cluster's radius)
    ax8 = plt.subplot(gs1[4:6, 2:4])
    #Set plot limits
    plt.xlim(col1_min, col1_max)
    plt.ylim(mag_min, mag_max)
    #Set axis labels
    plt.xlabel('$' + x_ax + '$', fontsize=18)
    plt.ylabel('$' + y_ax + '$', fontsize=18)
    # Set minor ticks
    ax8.minorticks_on()
    # Only draw units on axis (ie: 1, 2, 3)
    ax8.xaxis.set_major_locator(MultipleLocator(1.0))
    # Set grid
    ax8.grid(b=True, which='major', color='gray', linestyle='--', lw=1)
    tot_stars = len(stars_out_rjct) + len(stars_out)
    plt.text(0.53, 0.93, '$r > r_{cl}\,|\,N=%d$' % tot_stars,
        transform=ax8.transAxes, bbox=dict(facecolor='white', alpha=0.5),
        fontsize=16)
    # Plot stars.
    stars_rjct_temp = [[], []]
    for star in stars_out_rjct:
        stars_rjct_temp[0].append(star[5])
        stars_rjct_temp[1].append(star[3])
    plt.scatter(stars_rjct_temp[0], stars_rjct_temp[1], marker='x', c='teal',
                s=10, zorder=1)
    stars_acpt_temp = [[], []]
    for star in stars_out:
        stars_acpt_temp[0].append(star[5])
        stars_acpt_temp[1].append(star[3])
    sz_pt = 0.2 if (len(stars_out_rjct) + len(stars_out)) > 5000 else 0.5
    plt.scatter(stars_acpt_temp[0], stars_acpt_temp[1], marker='o', c='k',
                s=sz_pt, zorder=2)

    # Cluster's stars CMD (stars inside cluster's radius)
    ax9 = plt.subplot(gs1[4:6, 4:6])
    #Set plot limits
    plt.xlim(col1_min, col1_max)
    plt.ylim(mag_min, mag_max)
    #Set axis labels
    plt.xlabel('$' + x_ax + '$', fontsize=18)
    plt.ylabel('$' + y_ax + '$', fontsize=18)
    # Set minor ticks
    ax9.minorticks_on()
    # Only draw units on axis (ie: 1, 2, 3)
    ax9.xaxis.set_major_locator(MultipleLocator(1.0))
    # Set grid
    ax9.grid(b=True, which='major', color='gray', linestyle='--', lw=1)
    # Calculate total number of stars whitin cluster's radius.
    tot_stars = len(stars_in_rjct) + len(stars_in)
    plt.text(0.55, 0.93, '$r \leq r_{cl}\,|\,N=%d$' % tot_stars,
             transform=ax9.transAxes,
             bbox=dict(facecolor='white', alpha=0.5), fontsize=16)
    # Plot stars.
    stars_rjct_temp = [[], []]
    for star in stars_in_rjct:
        stars_rjct_temp[0].append(star[5])
        stars_rjct_temp[1].append(star[3])
    plt.scatter(stars_rjct_temp[0], stars_rjct_temp[1], marker='x', c='teal',
                s=12, zorder=1)
    stars_acpt_temp = [[], []]
    for star in stars_in:
        stars_acpt_temp[0].append(star[5])
        stars_acpt_temp[1].append(star[3])
    sz_pt = 0.5 if (len(stars_in_rjct) + len(stars_in)) > 1000 else 1.
    plt.scatter(stars_acpt_temp[0], stars_acpt_temp[1], marker='o', c='k',
                s=sz_pt, zorder=2)

    # Magnitude error
    ax10 = plt.subplot(gs1[4, 6:8])
    #Set plot limits
    plt.xlim(min(mag_data) - 0.5, max(mag_data) + 0.5)
    plt.ylim(-0.005, e_max + 0.01)
    #Set axis labels
    plt.ylabel('$\sigma_{' + y_ax + '}$', fontsize=18)
    plt.xlabel('$' + y_ax + '$', fontsize=18)
    # Set minor ticks
    ax10.minorticks_on()
    mag_x = np.linspace(min(mag_data), max(mag_data), 50)
    # Condition to not plot the lines if the fit was rejected.
    # Plot lower envelope.
    ax10.plot(mag_x, func(mag_x, *popt_mag), 'r-', zorder=3)
    if not rjct_errors_fit:
        # Plot left side of upper envelope (exponential).
        ax10.plot(mag_val_left, func(mag_val_left, *popt_umag), 'r--', lw=2.,
                 zorder=3)
        # Plot right side of upper envelope (polynomial).
        ax10.plot(mag_val_right, np.polyval(pol_mag, (mag_val_right)),
                 'r--', lw=2., zorder=3)
    # Plot rectangle.
    ax10.vlines(x=bright_end + 0.05, ymin=-0.005, ymax=be_e, color='r',
               linestyles='dashed', zorder=2)
    ax10.vlines(x=min(mag_data) - 0.05, ymin=-0.005, ymax=be_e, color='r',
               linestyles='dashed', zorder=2)
    ax10.hlines(y=be_e, xmin=min(mag_data), xmax=bright_end, color='r',
               linestyles='dashed', zorder=2)
    # Plot stars.
    stars_rjct_temp = [[], []]
    for star in stars_out_rjct:
        stars_rjct_temp[0].append(star[3])
        stars_rjct_temp[1].append(star[4])
    for star in stars_in_rjct:
        stars_rjct_temp[0].append(star[3])
        stars_rjct_temp[1].append(star[4])
    plt.scatter(stars_rjct_temp[0], stars_rjct_temp[1], marker='x', c='teal',
                s=15, zorder=1)
    stars_acpt_temp = [[], []]
    for star in stars_out:
        stars_acpt_temp[0].append(star[3])
        stars_acpt_temp[1].append(star[4])
    for star in stars_in:
        stars_acpt_temp[0].append(star[3])
        stars_acpt_temp[1].append(star[4])
    plt.scatter(stars_acpt_temp[0], stars_acpt_temp[1], marker='o', c='k',
                s=1, zorder=2)

    # Color error
    ax11 = plt.subplot(gs1[5, 6:8])
    #Set plot limits
    plt.xlim(min(mag_data) - 0.5, max(mag_data) + 0.5)
    plt.ylim(-0.005, e_max + 0.01)
    #Set axis labels
    plt.ylabel('$\sigma_{' + x_ax + '}$', fontsize=18)
    plt.xlabel('$' + y_ax + '$', fontsize=18)
    # Set minor ticks
    ax11.minorticks_on()
    # Condition to not plot the lines if the fit was rejected.
    # Plot lower envelope.
    ax11.plot(mag_x, func(mag_x, *popt_col1), 'r-', zorder=3)
    if not rjct_errors_fit:
        # Plot left side of upper envelope (exponential).
        ax11.plot(col1_val_left, func(col1_val_left, *popt_ucol1), 'r--', lw=2.,
                 zorder=3)
        # Plot right side of upper envelope (polynomial).
        ax11.plot(col1_val_right, np.polyval(pol_col1, (col1_val_right)),
                 'r--', lw=2., zorder=3)
    # Plot rectangle.
    ax11.vlines(x=bright_end + 0.05, ymin=-0.005, ymax=be_e, color='r',
               linestyles='dashed', zorder=2)
    ax11.vlines(x=min(mag_data) - 0.05, ymin=-0.005, ymax=be_e, color='r',
               linestyles='dashed', zorder=2)
    ax11.hlines(y=be_e, xmin=min(mag_data), xmax=bright_end, color='r',
               linestyles='dashed', zorder=2)
    # Plot stars.
    stars_rjct_temp = [[], []]
    for star in stars_out_rjct:
        stars_rjct_temp[0].append(star[3])
        stars_rjct_temp[1].append(star[6])
    for star in stars_in_rjct:
        stars_rjct_temp[0].append(star[3])
        stars_rjct_temp[1].append(star[6])
    plt.scatter(stars_rjct_temp[0], stars_rjct_temp[1], marker='x', c='teal',
                s=15, zorder=1)
    stars_acpt_temp = [[], []]
    for star in stars_out:
        stars_acpt_temp[0].append(star[3])
        stars_acpt_temp[1].append(star[6])
    for star in stars_in:
        stars_acpt_temp[0].append(star[3])
        stars_acpt_temp[1].append(star[6])
    plt.scatter(stars_acpt_temp[0], stars_acpt_temp[1], marker='o', c='k',
                s=1, zorder=2)

    # LF of stars in cluster region and outside.
    ax12 = plt.subplot(gs1[6:8, 0:2])
    #Set plot limits
    x_min, x_max = min(mag_data) - 0.5, max(mag_data) + 0.5
    plt.xlim(x_max, x_min)
    ax12.minorticks_on()
    # Only draw units on axis (ie: 1, 2, 3)
    ax12.xaxis.set_major_locator(MultipleLocator(2.0))
    # Set grid
    ax12.grid(b=True, which='major', color='gray', linestyle='--', lw=1)
    #Set axis labels
    plt.xlabel('$' + y_ax + '$', fontsize=18)
    plt.ylabel('$log(N^{\star})$', fontsize=18)
    # Plot create lists with mag values.
    stars_out_temp = []
    for star in stars_out_rjct:
        stars_out_temp.append(star[3])
    for star in stars_out:
        stars_out_temp.append(star[3])
    stars_in_temp = []
    for star in stars_in_rjct:
        stars_in_temp.append(star[3])
    for star in stars_in:
        stars_in_temp.append(star[3])
    # Plot histograms.
    binwidth = 0.25
    plt.hist(stars_out_temp,
             bins=np.arange(int(x_min), int(x_max + binwidth), binwidth),
             log=True, histtype='step', label='$r  > r_{cl}$', color='b')
    plt.hist(stars_in_temp,
             bins=np.arange(int(x_min), int(x_max + binwidth), binwidth),
             log=True, histtype='step', label='$r \leq r_{cl}$', color='r')
    # Force y axis min to 1.
    plt.ylim(1., plt.ylim()[1])
    # Completeness maximum value.
    # completeness = [max_mag, bin_edges, max_indx, comp_perc]
    bin_edges, max_indx = completeness[1], completeness[2]
    mag_peak = bin_edges[max_indx]
    ax12.vlines(x=mag_peak, ymin=1., ymax=plt.ylim()[1], color='g',
        linestyles='dashed', lw=2., label='$' + y_ax + '_{compl}$', zorder=3)
    # Legends.
    leg11 = plt.legend(fancybox=True, loc='upper right', numpoints=1,
                       fontsize=16)
    # Set the alpha value of the legend.
    leg11.get_frame().set_alpha(0.7)

    ax13 = plt.subplot(gs1[6:8, 2:4])
    # If field lists are not empty.
    if fl_reg_mag[0].any() and fl_reg_col[0].any():
        x_min = min(min(cl_reg_mag[0]), min(fl_reg_mag[0]),
            min(cl_reg_col[0]), min(fl_reg_col[0])) - 0.2
        x_max = max(max(cl_reg_mag[0]), max(fl_reg_mag[0]),
            max(cl_reg_col[0]), max(fl_reg_col[0])) + 0.2
        y_min = max(max(cl_reg_mag[1]), max(fl_reg_mag[1]),
            max(cl_reg_col[1]), max(fl_reg_col[1])) + 0.2
        y_max = min(min(cl_reg_mag[1]), min(fl_reg_mag[1]),
            min(cl_reg_col[1]), min(fl_reg_col[1])) - 0.2
    else:
        x_min, x_max = min(min(cl_reg_mag[0]), min(cl_reg_col[0])) - 0.2,\
        max(max(cl_reg_mag[0]), max(cl_reg_col[0])) + 0.2
        y_min, y_max = max(max(cl_reg_mag[1]), max(cl_reg_col[1])) + 0.2,\
        min(min(cl_reg_mag[1]), min(cl_reg_col[1])) - 0.2
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    #ax13.set_xlabel('$' + y_ax + '$', fontsize=18)
    #ax13.set_ylabel('$' + y_ax + '^*$', fontsize=18)
    ax13.set_xlabel('$mag$', fontsize=18)
    ax13.set_ylabel('$mag^*$', fontsize=18)
    #ax13.minorticks_on()
    ax13.grid(b=True, which='major', color='gray', linestyle='--', lw=1)
    # Text.
    text1 = '$' + y_ax + '^{*}_{cl+fl}$'
    text2 = '$' + y_ax + '^{*}_{fl}$'
    text3 = '$' + y_ax + '^{*}_{cl} = %0.2f$' % integ_mag
    if sys_select == 'UBVI':
        x_ax0 = 'B'
    elif sys_select == 'WASH':
        x_ax0 = 'C'
    text4 = '$' + x_ax0 + '^{*}_{cl+fl}$'
    text5 = '$' + x_ax0 + '^{*}_{fl}$'
    text6 = '$' + x_ax0 + '^{*}_{cl} = %0.2f$' % integ_col
    # Completeness maximum value.
    # completeness = [max_mag, bin_edges, max_indx, comp_perc]
    #bin_edges, max_indx = completeness[1], completeness[2]
    #mag_peak = bin_edges[max_indx]
    #ax13.vlines(x=mag_peak, ymin=y_min, ymax=y_max, color='g',
           #linestyles='dashed', lw=2., zorder=3)
    # Cluster + field integrated magnitude curve.
    plt.plot(cl_reg_mag[0], cl_reg_mag[1], 'r-', lw=1., label=text1)
    # Field average integrated magnitude curve.
    plt.plot(fl_reg_mag[0], fl_reg_mag[1], 'b-', lw=1., label=text2)
    # Cluster integrated magnitude value.
    plt.hlines(y=integ_mag, xmin=x_min, xmax=x_max, color='g',
               linestyles='dashed', lw=2., label=text3)
    # Cluster integrated magnitude.
    plt.plot(cl_reg_col[0], cl_reg_col[1], 'r:', lw=2., label=text4)
    # Field average integrated magnitude.
    plt.plot(fl_reg_col[0], fl_reg_col[1], 'b:', lw=2., label=text5)
    # Cluster integrated second magnitude value.
    plt.hlines(y=integ_col, xmin=x_min, xmax=x_max, color='k',
               linestyles='dashed', lw=2., label=text6)
    # ask matplotlib for the plotted objects and their labels
    lines, labels = ax13.get_legend_handles_labels()
    leg = ax13.legend(lines, labels, loc='lower right', numpoints=1,
        fontsize=11)
    leg.get_frame().set_alpha(0.75)

    ## Color integrated magnitude.
    #tempax = ax13.twinx()
    #ax132 = tempax.twiny()
    ## If lists are not empty.
    #if fl_reg_col[0].any():
        #x_min, x_max = min(min(cl_reg_col[0]), min(fl_reg_col[0])) - 0.2,\
            #max(max(cl_reg_col[0]), max(fl_reg_col[0])) + 0.2
        #y_min, y_max = max(max(cl_reg_col[1]), max(fl_reg_col[1])) + 0.2,\
            #min(min(cl_reg_col[1]), min(fl_reg_col[1])) - 0.2
        ##min_fl_col = min(fl_reg_col[1])
    #else:
        #x_min, x_max = min(cl_reg_col[0]) - 0.2, max(cl_reg_col[0]) + 0.2
        #y_min, y_max = max(cl_reg_col[1]) + 0.2, min(cl_reg_col[1]) - 0.2
        ##min_fl_col = 0.
    #ax132.set_xlabel('$' + x_ax + '$', fontsize=14)
    #tempax.set_ylabel('$' + x_ax + '^*$', fontsize=14, rotation=90)
    ## Text.
    #text4 = '$' + x_ax + '^{*}_{cl+fl}$'
    #text5 = '$' + x_ax + '^{*}_{fl}$'
    ## Cluster integrated magnitude.
    #plt.plot(cl_reg_col[0], cl_reg_col[1], 'r:', lw=2., label=text4)
    ## Field average integrated magnitude.
    #plt.plot(fl_reg_col[0], fl_reg_col[1], 'b:', lw=2., label=text5)
    #ax132.set(ylim=[y_min, y_max])
    ## ask matplotlib for the plotted objects and their labels
    #lines, labels = ax13.get_legend_handles_labels()
    #lines2, labels2 = ax132.get_legend_handles_labels()
    #leg = ax132.legend(lines + lines2, labels + labels2, loc='lower right',
        #numpoints=1, fontsize=12)
    #leg.get_frame().set_alpha(0.75)

    # Distribution of p_values.
    # pval_test_params[-1] is the flag that indicates if the block was
    # processed.
    if pval_test_params[-1]:
        # Extract parameters from list.
        prob_cl_kde, p_vals_cl, p_vals_f, kde_cl_1d, kde_f_1d, x_kde, y_over\
        = pval_test_params[:-1]
        ax14 = plt.subplot(gs1[6:8, 4:6])
        plt.xlim(-0.5, 1.5)
        plt.ylim(0, max(max(kde_f_1d), max(kde_cl_1d)) + 0.5)
        plt.xlabel('p-values', fontsize=12)
        ax14.minorticks_on()
        ax14.grid(b=True, which='major', color='gray', linestyle='--', lw=1)
        # Grid to background.
        ax14.set_axisbelow(True)
        # Plot cluster vs field KDE.
        plt.plot(x_kde, kde_cl_1d, c='b', ls='-', lw=1., label='$KDE_{cl}$')
        # Plot field vs field KDE.
        plt.plot(x_kde, kde_f_1d, c='r', ls='-', lw=1., label='$KDE_{f}$')
        # Fill overlap.
        plt.fill_between(x_kde, y_over, 0, color='grey', alpha='0.5')
        text = '$P_{cl}^{KDE} = %0.2f$' % round(prob_cl_kde, 2)
        plt.text(0.05, 0.92, text, transform=ax14.transAxes,
             bbox=dict(facecolor='white', alpha=0.6), fontsize=12)
        # Legend.
        handles, labels = ax14.get_legend_handles_labels()
        leg = ax14.legend(handles, labels, loc='upper right', numpoints=1,
                          fontsize=12)
        leg.get_frame().set_alpha(0.6)

        # QQ-plot.
        # Extract parameters from list.
        ccc, quantiles = qq_params
        ax15 = plt.subplot(gs1[6:8, 6:8])
        plt.xlim(-0.05, 1.05)
        plt.ylim(-0.05, 1.05)
        plt.xlabel('$p-value_{cl}$', fontsize=16)
        plt.ylabel('$p-value_{f}$', fontsize=16)
        ax15.minorticks_on()
        ax15.grid(b=True, which='major', color='gray', linestyle='--', lw=1)
        text = '$CCC\, = %0.2f$' % ccc
        plt.text(0.05, 0.92, text, transform=ax15.transAxes,
             bbox=dict(facecolor='white', alpha=0.85), fontsize=12)
        # Plot quantiles.
        plt.scatter(quantiles[0], quantiles[1], marker='o', c='k', s=10.)
        # Identity line.
        plt.plot([0., 1.], [0., 1.], color='k', linestyle='--', linewidth=1.)

    # Norm fit for decontamination algorithm probability values.
    # Check if decont algorithm was applied.
    plot_colorbar = False
    if not(flag_area_stronger):
        ax16 = plt.subplot(gs1[8:10, 0:2])
        plt.xlim(0., 1.)
        plt.xlabel('membership prob', fontsize=12)
        ax16.minorticks_on()
        ax16.grid(b=True, which='major', color='gray', linestyle='--', lw=1)
        prob_data = [star[7] for star in memb_prob_avrg_sort]
        # Best Gaussian fit of data.
        (mu, sigma) = stats.norm.fit(prob_data)
        # Text.
        text = '$\mu=%.3f,\ \sigma=%.3f$' % (mu, sigma)
        plt.text(0.05, 0.92, text, transform=ax16.transAxes,
             bbox=dict(facecolor='white', alpha=0.85), fontsize=12)
        # Histogram of the data.
        n, bins, patches = plt.hist(prob_data, 25, normed=1, color='green')
        # Best fit line.
        y = mlab.normpdf(bins, mu, sigma)
        plt.plot(bins, y, 'r--', linewidth=2)

        # Finding chart of cluster region with decontamination algorithm
        # applied.
        # Used for the finding chart with colors assigned according to the
        # probabilities obtained.
        # Check if decont algorithm was applied.
        ax17 = plt.subplot(gs1[8:10, 2:4])
        # Get max and min values in x,y
        x_min, x_max = 10000., -10000
        y_min, y_max = 10000., -10000
        for star in cluster_region:
            x_min, x_max = min(star[1], x_min), max(star[1], x_max)
            y_min, y_max = min(star[2], y_min), max(star[2], y_max)
        #Set plot limits
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
        #Set axis labels
        plt.xlabel('x (px)', fontsize=12)
        plt.ylabel('y (px)', fontsize=12)
        # Set minor ticks
        ax17.minorticks_on()
        # Radius
        circle = plt.Circle((center_cl[0], center_cl[1]), clust_rad,
                            color='red', fill=False)
        fig.gca().add_artist(circle)
        plt.text(0.63, 0.93, 'Cluster region', transform=ax17.transAxes,
            bbox=dict(facecolor='white', alpha=0.8), fontsize=12)
        # Color map, higher prob stars look redder.
        cm = plt.cm.get_cmap('RdYlBu_r')
        # Star sizes for dense and not dense regions.
        star_size = 20 if backg_value > 0.005 else 35
        m_p_m_temp = [[], [], []]
        for star in memb_prob_avrg_sort:
            m_p_m_temp[0].append(star[1])
            m_p_m_temp[1].append(star[2])
            m_p_m_temp[2].append(star[7])
        # Create new list with inverted values so higher prob stars are on top.
        m_p_m_temp_inv = [i[::-1] for i in m_p_m_temp]
        plt.scatter(m_p_m_temp_inv[0], m_p_m_temp_inv[1], marker='o',
                    c=m_p_m_temp_inv[2], s=star_size, edgecolors='black',
                    cmap=cm, lw=0.5)
        out_clust_rad = [[], []]
        for star in cluster_region:
            dist = np.sqrt((center_cl[0] - star[1]) ** 2 +
            (center_cl[1] - star[2]) ** 2)
            # Only plot stars outside the cluster's radius.
            if dist >= clust_rad:
                out_clust_rad[0].append(star[1])
                out_clust_rad[1].append(star[2])
        plt.scatter(out_clust_rad[0], out_clust_rad[1], marker='o',
                    s=star_size, edgecolors='black', facecolors='none', lw=0.5)

        # Star's membership probabilities on cluster's CMD.
        ax18 = plt.subplot(gs1[8:10, 4:6])
        #Set plot limits
        plt.xlim(col1_min, col1_max)
        plt.ylim(mag_min, mag_max)
        #Set axis labels
        plt.xlabel('$' + x_ax + '$', fontsize=18)
        plt.ylabel('$' + y_ax + '$', fontsize=18)
        tot_clust = len(memb_prob_avrg_sort)
        text = '$r \leq r_{cl}\,|\,N=%d$' % tot_clust
        plt.text(0.5, 0.93, text, transform=ax18.transAxes,
                 bbox=dict(facecolor='white', alpha=0.5), fontsize=16)
        # Set minor ticks
        ax18.minorticks_on()
        ax18.xaxis.set_major_locator(MultipleLocator(1.0))
        ax18.grid(b=True, which='major', color='gray', linestyle='--', lw=1)
        if bf_flag:
            # Plot isochrone if best fit process was used.
            plt.plot(shift_isoch[0], shift_isoch[1], 'g', lw=1.2)
        # This reversed colormap means higher prob stars will look redder.
        cm = plt.cm.get_cmap('RdYlBu_r')
        m_p_m_temp = [[], [], []]
        for star in memb_prob_avrg_sort:
            m_p_m_temp[0].append(star[5])
            m_p_m_temp[1].append(star[3])
            m_p_m_temp[2].append(star[7])
        # Create new list with inverted values so higher prob stars are on top.
        m_p_m_temp_inv = [i[::-1] for i in m_p_m_temp]
        v_min_mp, v_max_mp = round(min(m_p_m_temp[2]), 2), \
        round(max(m_p_m_temp[2]), 2)
        sca = plt.scatter(m_p_m_temp_inv[0], m_p_m_temp_inv[1], marker='o',
                    c=m_p_m_temp_inv[2], s=40, cmap=cm, lw=0.5, vmin=v_min_mp,
                    vmax=v_max_mp)
        # If list is not empty.
        if m_p_m_temp_inv[1]:
            # Plot error bars at several mag values.
            mag_y = np.arange(int(min(m_p_m_temp_inv[1]) + 0.5),
                              int(max(m_p_m_temp_inv[1]) + 0.5) + 0.1)
            x_val = [min(x_max_cmd, max(col1_data) + 0.2) - 0.4] * len(mag_y)
            plt.errorbar(x_val, mag_y, yerr=func(mag_y, *popt_mag),
                         xerr=func(mag_y, *popt_col1), fmt='k.', lw=0.8,
                         ms=0., zorder=4)
            # Plot colorbar (see bottom of file).
            if v_min_mp != v_max_mp:
                plot_colorbar = True

        # Synthetic cluster.
        if bf_flag:
            ax19 = plt.subplot(gs1[8:10, 6:8])
            #Set plot limits
            plt.xlim(col1_min, col1_max)
            plt.ylim(mag_min, mag_max)
            #Set axis labels
            plt.xlabel('$' + x_ax + '$', fontsize=18)
            plt.ylabel('$' + y_ax + '$', fontsize=18)
            # Set minor ticks
            ax19.minorticks_on()
            ax19.xaxis.set_major_locator(MultipleLocator(1.0))
            ax19.grid(b=True, which='major', color='gray', linestyle='--', lw=1)
            # Add text box
            m, a, e, d = isoch_fit_params[0]
            e_m, e_a, e_e, e_d = isoch_fit_errors
            text1 = '$z = %0.4f \pm %0.4f$' '\n' % (m, e_m)
            text2 = '$log(age) = %0.2f \pm %0.2f$' '\n' % (a, e_a)
            text3 = '$E_{(B-V)} = %0.2f \pm %0.2f$' '\n' % (e, e_e)
            text4 = '$(m-M)_o = %0.2f \pm %0.2f$' % (d, e_d)
            text = text1 + text2 + text3 + text4
            plt.text(0.5, 0.77, text, transform=ax19.transAxes,
                     bbox=dict(facecolor='white', alpha=0.6), fontsize=12)
            # Plot isochrone.
            plt.plot(shift_isoch[0], shift_isoch[1], 'r', lw=1.2)
            # Plot synth clust.
            plt.scatter(synth_clst[0], synth_clst[2], marker='o', s=30,
                        c='#4682b4', lw=0.5)

    # Best fitting process plots for GA.
    if bf_flag and best_fit_algor == 'genet':

        # Set ranges used by plots below.
        m_min, m_max = m_rs
        a_min, a_max = a_rs
        e_min, e_max = e_rs
        d_min, d_max = d_rs
        if m_min == m_max:
            m_min, m_max = m_min - 0.1 * m_min, m_max + 0.1 * m_min
        if a_min == a_max:
            a_min, a_max = a_min - 0.1 * a_min, a_max + 0.1 * a_min
        if e_min == e_max:
            e_min, e_max = e_min - 0.1 * e_min, e_max + 0.1 * e_min
        if d_min == d_max:
            d_min, d_max = d_min - 0.1 * d_min, d_max + 0.1 * d_min

        # Age vs metallicity GA diagram.
        isoch_done = isoch_fit_params[3]
        plt.subplot(gs1[10:12, 0:2])
        # Axis limits.
        plt.xlim(m_min, m_max)
        plt.ylim(a_min, a_max)
        plt.xlabel('$z$', fontsize=16)
        plt.ylabel('$log(age)$', fontsize=16)
        # Plot best fit point.
        plt.scatter(m, a, marker='o', c='r', s=30)
        # Plot ellipse error.
        ax20 = plt.gca()
        ellipse = Ellipse(xy=(m, a), width=2 * e_m, height=2 * e_a,
                                edgecolor='r', fc='None', lw=1.)
        ax20.add_patch(ellipse)
        # Plot density map.
        hist, xedges, yedges = np.histogram2d(zip(*isoch_done[0])[0],
                                              zip(*isoch_done[0])[1], bins=100)
        # H_g is the 2D histogram with a gaussian filter applied
        h_g = gaussian_filter(hist, 2, mode='constant')
        plt.imshow(h_g.transpose(), origin='lower',
                   extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
                   cmap=plt.get_cmap('Blues'), aspect='auto')

        # GA diagram.
        lkl_old, ext_imm_indx = isoch_fit_params[1], isoch_fit_params[2]
        ax21 = plt.subplot(gs1[10:12, 2:6])
        plt.xlim(-0.5, n_gen + int(0.01 * n_gen))
        plt.ylim(max(0, min(lkl_old[0]) - 0.3 * min(lkl_old[0])),
                 max(lkl_old[1]) + min(lkl_old[0]) / 2.)
        ax21.tick_params(axis='y', which='major', labelsize=9)
        ax21.grid(b=True, which='major', color='gray', linestyle='--', lw=0.6)
        plt.xlabel('Generation', fontsize=12)
        plt.ylabel('Likelihood', fontsize=12)
        text1 = '$N = %d\,;\,L_{min}=%0.2f$' '\n' % (len(lkl_old[0]),
            min(lkl_old[0]))
        text2 = '$n_{gen}=%d\,;\,n_{pop}=%d$' '\n' % (n_gen, n_pop)
        text3 = '$f_{dif}=%0.2f\,;\,cr_{sel}=%s$' '\n' % (fdif, cr_sel)
        text4 = '$p_{cross}=%0.2f\,;\,p_{mut}=%0.2f$' '\n' % (p_cross, p_mut)
        text5 = '$n_{el}=%d\,;\,n_{ei}=%d\,;\,n_{es}=%d$' % (n_el, n_ei, n_es)
        text = text1 + text2 + text3 + text4 + text5
        plt.text(0.05, 0.75, text, transform=ax21.transAxes,
            bbox=dict(facecolor='white', alpha=0.75), fontsize=12)
        # Plot likelihood minimum and mean lines.
        ax21.plot(range(len(lkl_old[0])), lkl_old[0], lw=1., c='black',
                  label='$L_{min}$')
        ax21.plot(range(len(lkl_old[0])), lkl_old[1], lw=1., c='blue',
                  label='$L_{mean}$')
        # Plot extinction/immigration lines.
        for lin in ext_imm_indx:
            plt.axvline(x=lin, linestyle='--', lw=2., color='green')
        # Legend.
        handles, labels = ax21.get_legend_handles_labels()
        leg = ax21.legend(handles, labels, loc='upper right', numpoints=1,
                          fontsize=12)
        leg.get_frame().set_alpha(0.6)

        # Extinction vs distance modulus GA diagram.
        isoch_done = isoch_fit_params[3]
        plt.subplot(gs1[10:12, 6:8])
        plt.xlim(e_min, e_max)
        plt.ylim(d_min, d_max)
        plt.xlabel('$E_{(B-V)}$', fontsize=16)
        plt.ylabel('$(m-M)_o$', fontsize=16)
        # Plot best fit point.
        plt.scatter(e, d, marker='o', c='b', s=30)
        # Plot ellipse error.
        ax21 = plt.gca()
        ellipse = Ellipse(xy=(e, d), width=2 * e_e, height=2 * e_d,
                                edgecolor='b', fc='None', lw=1.)
        ax21.add_patch(ellipse)
        # Plot density map.
        hist, xedges, yedges = np.histogram2d(zip(*isoch_done[0])[2],
                                              zip(*isoch_done[0])[3], bins=100)
        # H_g is the 2D histogram with a gaussian filter applied
        h_g = gaussian_filter(hist, 2, mode='constant')
        plt.imshow(h_g.transpose(), origin='lower',
                   extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
                   cmap=plt.get_cmap('Reds'), aspect='auto')

        ax22 = plt.subplot(gs1[12:14, 0:2])
        plt.ylim(max(0, min(lkl_old[0]) - 0.3 * min(lkl_old[0])),
            max(lkl_old[1]))
        plt.xlim(m_min, m_max)
        ax22.tick_params(axis='y', which='major', labelsize=9)
        plt.ylabel('Likelihood', fontsize=12)
        plt.xlabel('$z$', fontsize=16)
        text = '$z = %0.4f \pm %0.4f$' % (m, e_m)
        plt.text(0.1, 0.93, text, transform=ax22.transAxes,
            bbox=dict(facecolor='white', alpha=0.5), fontsize=12)
        hist, xedges, yedges = np.histogram2d(zip(*isoch_done[0])[0],
                                              isoch_done[1], bins=100)
        # H_g is the 2D histogram with a gaussian filter applied
        h_g = gaussian_filter(hist, 2, mode='constant')
        y_min_edge = max(0, min(lkl_old[0]) - 0.3 * min(lkl_old[0]))
        plt.imshow(h_g.transpose(), origin='lower',
                   extent=[xedges[0], xedges[-1], y_min_edge, yedges[-1]],
                   cmap=plt.get_cmap('gist_yarg'), aspect='auto')
        plt.axvline(x=m, linestyle='--', color='blue')
        plt.axvline(x=m + e_m, linestyle='--', color='red')
        plt.axvline(x=m - e_m, linestyle='--', color='red')

        ax23 = plt.subplot(gs1[12:14, 2:4])
        plt.ylim(max(0, min(lkl_old[0]) - 0.3 * min(lkl_old[0])),
            max(lkl_old[1]))
        plt.xlim(a_min, a_max)
        ax23.tick_params(axis='y', which='major', labelsize=9)
        plt.ylabel('Likelihood', fontsize=12)
        plt.xlabel('$log(age)$', fontsize=16)
        text = '$log(age) = %0.2f \pm %0.2f$' % (a, e_a)
        plt.text(0.1, 0.93, text, transform=ax23.transAxes,
            bbox=dict(facecolor='white', alpha=0.5), fontsize=12)
        hist, xedges, yedges = np.histogram2d(zip(*isoch_done[0])[1],
                                              isoch_done[1], bins=100)
        # H_g is the 2D histogram with a gaussian filter applied
        h_g = gaussian_filter(hist, 2, mode='constant')
        plt.imshow(h_g.transpose(), origin='lower',
                   extent=[xedges[0], xedges[-1], y_min_edge, yedges[-1]],
                   cmap=plt.get_cmap('gist_yarg'), aspect='auto')
        plt.axvline(x=a, linestyle='--', color='blue')
        plt.axvline(x=a + e_a, linestyle='--', color='red')
        plt.axvline(x=a - e_a, linestyle='--', color='red')

        ax24 = plt.subplot(gs1[12:14, 4:6])
        plt.ylim(max(0, min(lkl_old[0]) - 0.3 * min(lkl_old[0])),
            max(lkl_old[1]))
        plt.xlim(e_min, e_max)
        ax24.tick_params(axis='y', which='major', labelsize=9)
        plt.ylabel('Likelihood', fontsize=12)
        plt.xlabel('$E_{(B-V)}$', fontsize=16)
        text = '$E_{(B-V)} = %0.2f \pm %0.2f$' % (e, e_e)
        plt.text(0.1, 0.93, text, transform=ax24.transAxes,
            bbox=dict(facecolor='white', alpha=0.5), fontsize=12)
        hist, xedges, yedges = np.histogram2d(zip(*isoch_done[0])[2],
                                              isoch_done[1], bins=100)
        # H_g is the 2D histogram with a gaussian filter applied
        h_g = gaussian_filter(hist, 2, mode='constant')
        plt.imshow(h_g.transpose(), origin='lower',
                   extent=[xedges[0], xedges[-1], y_min_edge, yedges[-1]],
                   cmap=plt.get_cmap('gist_yarg'), aspect='auto')
        plt.axvline(x=e, linestyle='--', color='blue')
        plt.axvline(x=e + e_e, linestyle='--', color='red')
        plt.axvline(x=e - e_e, linestyle='--', color='red')

        ax25 = plt.subplot(gs1[12:14, 6:8])
        plt.ylim(max(0, min(lkl_old[0]) - 0.3 * min(lkl_old[0])),
            max(lkl_old[1]))
        plt.xlim(d_min, d_max)
        ax25.tick_params(axis='y', which='major', labelsize=9)
        plt.ylabel('Likelihood', fontsize=12)
        plt.xlabel('$(m-M)_o$', fontsize=16)
        text = '$(m-M)_o = %0.2f \pm %0.2f$' % (d, e_d)
        plt.text(0.1, 0.93, text, transform=ax25.transAxes,
            bbox=dict(facecolor='white', alpha=0.5), fontsize=12)
        hist, xedges, yedges = np.histogram2d(zip(*isoch_done[0])[3],
                                              isoch_done[1], bins=100)
        # H_g is the 2D histogram with a gaussian filter applied
        h_g = gaussian_filter(hist, 2, mode='constant')
        plt.imshow(h_g.transpose(), origin='lower',
                   extent=[xedges[0], xedges[-1], y_min_edge, yedges[-1]],
                   cmap=plt.get_cmap('gist_yarg'), aspect='auto')
        plt.axvline(x=d, linestyle='--', color='blue')
        plt.axvline(x=d + e_d, linestyle='--', color='red')
        plt.axvline(x=d - e_d, linestyle='--', color='red')

    # Ignore warning issued by colorbar plotted in CMD with membership
    # probabilities.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fig.tight_layout()

    # Plot colorbar down here so tight_layout won't move it around.
    if plot_colorbar is True:
        import matplotlib
        # Position and dimensions relative to the axes.
        x0, y0, width, height = [0.6, 0.85, 0.2, 0.04]
        # Transform them to get the ABSOLUTE POSITION AND DIMENSIONS
        Bbox = matplotlib.transforms.Bbox.from_bounds(x0, y0, width, height)
        trans = ax18.transAxes + fig.transFigure.inverted()
        l, b, w, h = matplotlib.transforms.TransformedBbox(Bbox, trans).bounds
        # Create the axes and the colorbar.
        cbaxes = fig.add_axes([l, b, w, h])
        cbar = plt.colorbar(sca, cax=cbaxes, ticks=[v_min_mp, v_max_mp],
            orientation='horizontal')
        cbar.ax.tick_params(labelsize=9)

    # Generate output file for each data file.
    pl_fmt = pl_params[1]
    pl_dpi = pl_params[2]
    plt.savefig(join(output_subdir, str(clust_name) + '.' + pl_fmt), dpi=pl_dpi)

    # Close to release memory.
    plt.clf()
    plt.close()