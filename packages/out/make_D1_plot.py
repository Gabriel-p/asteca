
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from os.path import join
from . import add_version_plot
from . import mp_mcmc_cnvrg
from . import tracePlot
from . import prep_plots
from . prep_plots import figsize_x, figsize_y, grid_x, grid_y


def main(npd, pd, isoch_fit_params, isoch_fit_errors, **kwargs):
    """
    Make D1 block plots.
    """
    if 'D1' in pd['flag_make_plot'] and pd['best_fit_algor'] != 'n':
        fig = plt.figure(figsize=(figsize_x, figsize_y))
        gs = gridspec.GridSpec(grid_y, grid_x)

        # Title and version for the plot.
        m_bf, s_bf = divmod(isoch_fit_params['bf_elapsed'], 60)
        h_bf, m_bf = divmod(m_bf, 60)

        xf, yf = .02, .999
        add_version_plot.main(x_fix=xf, y_fix=yf)

        nwalkers, nburn, nsteps, pt_adapt = pd['nwalkers_mcee'],\
            pd['nburn_mcee'], isoch_fit_params['N_steps'],\
            pd['pt_adapt']
        p_str = (
            "chains={:.0f}, burn={:.2f}, steps={:.0f},"
            " adapt={}").format(nwalkers, nburn, nsteps[-1], pt_adapt)

        xt, yt = .5, 1.005
        plt.suptitle(
            ("{} | {:.0f}h{:.0f}m").format(p_str, h_bf, m_bf), x=xt, y=yt,
            fontsize=11)

        # DEPRECATED May 2020
        # if pd['best_fit_algor'] == 'boot+GA':
        #     m_btsr, s_btsr = divmod(isoch_fit_params['btstrp_t'], 60)
        #     h_btsr, m_btsr = divmod(m_btsr, 60)
        #     p_str = (
        #         r"$N_{{pop}}={},\,N_{{gen}}={},\,N_{{btstrp}}={}$ "
        #         "({:.0f}h{:.0f}m)").format(
        #             pd['N_pop'], isoch_fit_params['OF_steps'],
        #             isoch_fit_params['N_bootstrap'], h_btsr, m_btsr)
        #     if isoch_fit_params['N_bootstrap'] == 0:
        #         xt = 0.83
        #         xf, yf = .67, 1.01
        # elif pd['best_fit_algor'] == 'ptemcee':
        # elif pd['best_fit_algor'] == 'emcee':
        #     nwalkers, nburn, nsteps = pd['nwalkers_mcee'],\
        #         pd['nburn_mcee'], isoch_fit_params['N_steps']
        #     p_str = (
        #         "[{}] chains={:.0f}, burn={:.2f}, steps={:.0f} ").format(
        #         ' '.join(pd['emcee_moves']), nwalkers, nburn, nsteps[-1])
        # Best fitting process plots.
        # if pd['best_fit_algor'] == 'boot+GA':

        #     if isoch_fit_params['N_bootstrap'] > 2:
        #         pos0 = (0, 2, 4, 8)
        #         pos1 = (
        #             (0, 2, 2, 4), (2, 4, 4, 6), (4, 6, 6, 8),
        #             (6, 8, 8, 10), (8, 10, 10, 12), (6, 8, 10, 12))
        #         min_max_p = prep_plots.param_ranges(
        #             pd['best_fit_algor'], pd['fundam_params'],
        #             isoch_fit_params['varIdxs'],
        #             isoch_fit_params['params_boot'])
        #         sharedPlots(pd, npd, isoch_fit_params, gs, min_max_p)
        #     else:
        #         pos0 = (0, 2, 8, 12)
        #         pos1 = (
        #             (2, 4, 8, 10), (2, 4, 10, 12), (4, 6, 8, 10),
        #             (4, 6, 10, 12), (6, 8, 8, 10), (6, 8, 10, 12))

        #     min_max_p = prep_plots.param_ranges(
        #         pd['best_fit_algor'], pd['fundam_params'])
        #     args = [
        #         # pl_GA_lkl: Likelihood evolution for the GA.
        #         gs, pos0, isoch_fit_params['lkl_best'],
        #         isoch_fit_params['lkl_mean'], isoch_fit_params['OF_models'],
        #         isoch_fit_params['new_bs_indx'], pd['fit_diff'],
        #         pd['cross_prob'], pd['cross_sel'], pd['mut_prob'],
        #         pd['N_el'], pd['N_ei'], pd['N_es']
        #     ]
        #     mp_best_fit1_GA.plot(0, *args)

        #     arglist = [
        #         # pl_lkl_scatt: Parameter likelihood density plot.
        #         [gs, pos1, r'$z$', min_max_p, isoch_fit_params['map_sol'],
        #          isoch_fit_errors, isoch_fit_params['models_GA'],
        #          isoch_fit_params['lkls_GA']],
        #         [gs, pos1, r'$log(age)$', min_max_p,
        #          isoch_fit_params['map_sol'], isoch_fit_errors,
        #          isoch_fit_params['models_GA'], isoch_fit_params['lkls_GA']],
        #         [gs, pos1, r'$E_{{(B-V)}}$', min_max_p,
        #          isoch_fit_params['map_sol'], isoch_fit_errors,
        #          isoch_fit_params['models_GA'], isoch_fit_params['lkls_GA']],
        #         [gs, pos1, r'$(m-M)_o$', min_max_p,
        #          isoch_fit_params['map_sol'], isoch_fit_errors,
        #          isoch_fit_params['models_GA'], isoch_fit_params['lkls_GA']],
        #         [gs, pos1, r'$M\,(M_{{\odot}})$', min_max_p,
        #          isoch_fit_params['map_sol'], isoch_fit_errors,
        #          isoch_fit_params['models_GA'], isoch_fit_params['lkls_GA']],
        #         [gs, pos1, r'$b_{{frac}}$', min_max_p,
        #          isoch_fit_params['map_sol'], isoch_fit_errors,
        #          isoch_fit_params['models_GA'], isoch_fit_params['lkls_GA']]
        #     ]
        #     for n, args in enumerate(arglist, 1):
        #         mp_best_fit1_GA.plot(n, *args)

        # elif pd['best_fit_algor'] in ('ptemcee', 'emcee'):  # 'abc'

        # Trace plots
        min_max_p = prep_plots.param_ranges(
            pd['fundam_params'], isoch_fit_params['varIdxs'],
            isoch_fit_params['pars_chains'])
        trace = isoch_fit_params['mcmc_trace']
        best_sol = isoch_fit_params['mean_sol']
        traceplot_args = (
            isoch_fit_params['acorr_t'],
            isoch_fit_params['med_at_c'], isoch_fit_params['mcmc_ess'])
        post_trace, pre_trace = isoch_fit_params['pars_chains'],\
            isoch_fit_params['pars_chains_bi']

        # pl_param_chain: Parameters sampler chains.
        par_list = ['metal', 'age', 'ext', 'dist', 'mass', 'binar']
        for p in par_list:
            args = [
                p, gs, best_sol, min_max_p, traceplot_args, trace,
                isoch_fit_params['varIdxs'], post_trace, pre_trace]
            tracePlot.plot(0, *args)

        # Parallel Coordinates plot
        # mp_mcmc_cnvrg.plot(2, *args)

        # pl_MAP_lkl: Parameters half of pdfs.
        args = [
            gs, isoch_fit_params['N_steps'], isoch_fit_params['prob_mean'],
            isoch_fit_params['map_lkl'], isoch_fit_params['map_lkl_final']]
        mp_mcmc_cnvrg.plot(0, *args)

        # if pd['best_fit_algor'] == 'ptemcee':
        # pl_betas: Betas vs steps.
        args = [
            gs, isoch_fit_params['Tmax'], isoch_fit_params['N_steps'],
            isoch_fit_params['betas_pt']]
        mp_mcmc_cnvrg.plot(2, *args)

        # pl_Tswaps: Tswaps AFs vs steps.
        args = [
            gs, isoch_fit_params['N_steps'], isoch_fit_params['tswaps_afs']]
        mp_mcmc_cnvrg.plot(3, *args)

        # pl_MAF: Parameters evolution of MAF.
        maf_steps = isoch_fit_params['maf_allT']
        # if pd['best_fit_algor'] == 'ptemcee':
        # elif pd['best_fit_algor'] == 'emcee':
        #     maf_steps = isoch_fit_params['maf_steps']
        args = [gs, isoch_fit_params['N_steps'], maf_steps]
        mp_mcmc_cnvrg.plot(1, *args)

        # pl_tau
        args = [
            gs, isoch_fit_params['N_steps'], isoch_fit_params['tau_autocorr']]
        mp_mcmc_cnvrg.plot(4, *args)

        # TODO re-implement when/if code is fixed
        # # pl_mESS
        # args = [
        #     'mESS', gs, isoch_fit_params['mESS'],
        #     isoch_fit_params['minESS'],
        #     isoch_fit_params['mESS_epsilon']]
        # mp_mcmc_cnvrg.plot(7, *args)

        # pl_lags
        args = [
            gs, isoch_fit_params['varIdxs'],
            isoch_fit_params['acorr_function']]
        mp_mcmc_cnvrg.plot(5, *args)

        # pl_GW
        args = [
            gs, isoch_fit_params['varIdxs'], isoch_fit_params['geweke_z']]
        mp_mcmc_cnvrg.plot(6, *args)

        # pl_tau_histo
        args = [gs, isoch_fit_params['all_taus']]
        mp_mcmc_cnvrg.plot(7, *args)

        # Generate output file.
        try:
            fig.tight_layout()
            plt.savefig(join(
                npd['output_subdir'], str(npd['clust_name']) + '_D1_' +
                pd['best_fit_algor']), bbox_inches='tight')
            print("<<Plots for D1 block created>>")
        except Exception as exc:
            print(exc)
            print("\n\n  ERROR: could not plot 'D1' block.\n")
        # Close to release memory.
        plt.clf()
        plt.close("all")
    else:
        print("<<Skip D1 block plot>>")


# def sharedPlots(pd, npd, isoch_fit_params, gs, min_max_p):
#     """
#     """

#     # DEPRECATED May 2020
#     # if pd['best_fit_algor'] == 'boot+GA':
#     #     trace = isoch_fit_params['params_boot']
#     #     msol = 'ML'
#     #     best_sol = isoch_fit_params['map_sol']
#     #     traceplot_args = []
#     #     post_trace, pre_trace = isoch_fit_params['params_boot'], None
#     # elif pd['best_fit_algor'] in ('ptemcee', 'emcee'):
