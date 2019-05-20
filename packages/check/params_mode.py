
import sys
from os.path import join, isfile
from os import extsep


def check(mypath, cl_files, run_mode, **kwargs):
    """
    Check that running mode parameters are properly written.
    """

    # Check mode.
    if run_mode not in ('auto', 'semi'):
        sys.exit("ERROR: 'mode' value selected ('{}') is not valid.".format(
            run_mode))

    semi_file = 'semi_input.dat'
    if run_mode == 'semi':
        # Check if semi_input.dat file exists.
        if not isfile(join(mypath, semi_file)):
            # File semi_input.dat does not exist.
            sys.exit("ERROR: 'semi' mode is set but 'semi_input.dat' file does"
                     " not exist.")

        for clust_path in cl_files:
            cl_split = clust_path[-1].split(extsep)
            clust_name = '.'.join(cl_split[:-1])
            # Flag to indicate if cluster was found in file.
            flag_clust_found = False
            with open(semi_file, "r") as f_cl_dt:
                for line in f_cl_dt:
                    li = line.strip()
                    # Skip comments.
                    if not li.startswith("#"):
                        reader = li.split()
                        # Prevent empty lines with spaces detected as a cluster
                        # line from crashing the code.
                        if reader:
                            # If cluster is found in file.
                            if reader[0] == clust_name:
                                # Set flag to True if the cluster was found.
                                flag_clust_found = True

            # Cluster not found.
            if not flag_clust_found:
                # Name of cluster not found in semi_input file.
                sys.exit("ERROR: 'semi' mode is set but '{}' was not found\n"
                         "in 'semi_input.dat' file".format(clust_name))
