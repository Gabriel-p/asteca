
import move_isochrone
import cut_max_mag
import mass_distribution
import mass_interp
import binarity
import completeness_rm
import add_errors

#############################################################
# # Timer function: http://stackoverflow.com/a/21860100/1391441
# from contextlib import contextmanager
# import time


# @contextmanager
# def timeblock(label):
#     start = time.clock()
#     try:
#         yield
#     finally:
#         end = time.clock()
#         print ('{} elapsed: {}'.format(label, end - start))
#############################################################


def main(err_max, bin_mass_ratio, err_lst, completeness, max_mag_syn,
         st_dist_mass, isochrone, R_V, ext_coefs, N_fc, synth_cl_params):
    """
    Takes an isochrone and returns a synthetic cluster created according to
    a certain mass distribution.

    The synthetic cluster returned has the shape:

    synth_clust = [photometry, binary_idxs, extra_pars]

    photometry = [photom, errors]
    photom = [f1, f2, ..., fF, c1, c2, ..., cC]
    (where F and C are the total number of filters and colors defined)

    errors = [ef1, ef2, ..., efF, ec1, ec2, ..., ecC]
    (photometric errrors for each photometric dimension defined)

    Correct indexes of binary systems after completeness removal.
    binary_idxs = [i1, i2, ..., iN]

    Six lists containing the theoretical tracks extra parameters.
    extra_pars = [l1, l2, ..., l6]
    """

    # Unpack synthetic cluster parameters. The first two elements are the
    # metallicity and the age, which are already incorporated in the selected
    # isochrone.
    e, d, M_total, bin_frac = synth_cl_params[2:]

    # with timeblock("move"):
    # Move theoretical isochrone using the values 'e' and 'd'.
    isoch_moved = move_isochrone.main(isochrone, e, d, R_V, ext_coefs, N_fc)

    ##############################################################
    # # To generate a synthetic cluster with the full isochrone length,
    # # un-comment this line.
    # # This takes the max magnitude from the isochrone itself instead of using
    # # the input cluster file.
    # print "\nCluster's log(age): {:0.2f}".format(synth_cl_params[1])
    # print 'Fixed total mass: {:0.2f}'.format(M_total)
    # max_mag = max(isoch_moved[1]) + 0.5
    ##############################################################

    # Get isochrone minus those stars beyond the magnitude cut.
    # with timeblock("cut"):
    isoch_cut = cut_max_mag.main(isoch_moved, max_mag_syn)

    # Empty list to pass if at some point no stars are left.
    synth_clust = []
    # Check for an empty array.
    if isoch_cut.any():

        # Store mass distribution used to produce a synthetic cluster based on
        # a given theoretic isochrone.
        # with timeblock("mass_dist"):
        mass_dist = mass_distribution.main(st_dist_mass, M_total)

        # Interpolate masses in mass_dist into the isochrone rejecting those
        # masses that fall outside of the isochrone's mass range.
        # with timeblock("interp"):
        isoch_mass = mass_interp.main(isoch_cut, mass_dist, N_fc)

        if isoch_mass.any():

            ##############################################################
            # # For plotting purposes: store a copy of this list before
            # # adding binaries since the list gets overwritten.
            # from copy import deepcopy
            # isoch_mass0 = deepcopy(isoch_mass)
            ##############################################################

            # Assignment of binarity.
            # with timeblock("binar"):
            isoch_binar, binar_idx0 = binarity.main(
                isoch_mass, isoch_cut, bin_frac, bin_mass_ratio, N_fc)

            # Completeness limit removal of stars.
            # with timeblock("compl"):
            isoch_compl, binar_idx = completeness_rm.main(
                isoch_binar, binar_idx0, completeness)

            ##############################################################
            # # Use when producing synthetic clusters from isochrones.
            # # Comment the line above.
            # isoch_compl = compl_func2(isoch_binar)
            ##############################################################

            if isoch_compl.any():

                # Get errors according to errors distribution.
                # with timeblock("errors"):
                synth_clust = add_errors.main(
                    isoch_compl, binar_idx, err_lst, err_max, N_fc)

    ################################################################
    # # Plot synthetic cluster.
    # from synth_plot import synth_clust_plot as s_c_p
    # m, a = synth_cl_params[:2]
    # print m, a, M_total
    # out_name = str(m).split('.')[1] + '_' + str(a)
    # # out_name = 'synth_clust'
    # out_folder = '/home/gabriel/Descargas/'
    # path = out_folder + out_name + '.png'
    # s_c_p(N_fc, mass_dist, isochrone, synth_cl_params, isoch_moved,
    #       isoch_cut, isoch_mass0, isoch_binar, binar_idx0, isoch_compl,
    #       binar_idx, synth_clust, path)
    ################################################################

    ################################################################
#     # Write synthetic cluster to file.
#     out_file_name = out_folder + out_name + '.dat'
#     with open(out_file_name, "w") as f_out:
#         f_out.write('''#color    e_col   magnitude     e_mag    init_mass''')
#         f_out.write('\n')
#     with open(out_file_name, "a") as f_out:
#         for line in zip(*synth_clust):
#                 f_out.write('''{:<8.3f} {:>8.3f} {:>8.3f} {:>8.3f} \
# {:>8.2f}\n'''.format(*map(float, line)))
    ################################################################

    return synth_clust