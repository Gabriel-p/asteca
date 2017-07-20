
import sys
from os.path import isfile
from packages.inp import names_paths


def check(cl_files, fld_rem_methods, bin_methods, bayesda_mode, fld_clean_mode,
          fld_clean_bin, **kwargs):
    """
    Check parameters related to the decontamination algorithm functions.
    """

    # Check decontamination algorithm parameters.
    # Check if 'mode' was correctly set.
    if bayesda_mode not in ['auto', 'manual', 'read', 'skip']:
        sys.exit("ERROR: Wrong name ('{}') for decontamination algorithm "
                 "'mode'.".format(bayesda_mode))

    if bayesda_mode == 'read':
        # Check if file exists.
        for cl_file in cl_files:

            # Get file name for membership files.
            memb_file = names_paths.memb_file_name(cl_file)
            if not isfile(memb_file):
                # File does not exist.
                sys.exit("ERROR: 'read' mode was set for decontamination "
                         "algorithm but the file:\n\n {}\n\ndoes not "
                         "exist.".format(memb_file))

    # Check 'field stars removal' method selected.
    if fld_clean_mode not in fld_rem_methods:
        sys.exit("ERROR: the selected field stars removal method ('{}')"
                 " does\nnot match a valid input.".format(fld_clean_mode))
    # Check binning if 'local' method was selected.
    if fld_clean_mode == 'local' and fld_clean_bin not in bin_methods:
        sys.exit("ERROR: the selected binning method '{}' for the 'Reduced"
                 "\nmembership' function does not match a valid input."
                 .format(fld_clean_bin))
