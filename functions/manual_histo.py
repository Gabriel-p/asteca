#import matplotlib.pyplot as plt
#import matplotlib.gridspec as gridspec


def manual_histo(id_star, xdata, ydata, T1_data, e_T1, CT1_data, e_CT1, 
                 xedges, yedges):
    
    ''' Obtains a (manual) 2D histogram for the field with not only the number
    of stars per bin but also the values associated to each of those stars: x, y
    coordinates and T1, eT1, CT1, eCT1 values.
    '''

    # Create the empty list that will hold the information of each star that
    # falls within a given bin in the 2D histogram.
    # H = [ [[num of stars in bin], [star 1 data (id,x,y,T1, etc..)],
    # [star 2 data], [star 3 data], ...], [], [], ..., [] ]
    H_manual = []
    for i in range(len(xedges)-1):
        H_manual.append([[0] for _ in xrange(len(yedges)-1)])
    
    # Iterate through all the stars in the frame.
    for xindex, xcoord in enumerate(xdata):
        ycoord = ydata[xindex]
        
        # Iterate through all edges in the x axis.
        for xbin_index, xitem_edg in enumerate(xedges):

            # Star contained by left border of bin in the x axis.
            if xcoord >= xitem_edg:
                try:
                # Check to see if a bin beyond this one exists.
                    xedges[xbin_index+1]
                except IndexError:
                # Bin doesn't exist so the star is located at the border of the
                # x axis.
                    # Iterate through all edges in the y axis.
                    for ybin_index, yitem_edg in enumerate(yedges):

                        # Star contained by bottom border of bin in the y axis.
                        if ycoord >= yitem_edg:
                            try:
                            # Check to see a bin beyond this one exists.
                                yedges[ybin_index+1]
                            except IndexError:
                            # Star located at the border of the y axis.
                                try:
                                # Check if the bin exists.
                                    H_manual[xbin_index][ybin_index]
                                except IndexError:
                                # Star outside of 2d hist list of bins. It
                                # happens for a couple of stars per frame, so we
                                # just iognore it.
                                    pass
                                else:
                                # Store the star's data and increase the count
                                # for this bin.
                                    H_manual[xbin_index][ybin_index][0] += 1
                                    H_manual[xbin_index][ybin_index].extend(\
                                    [[id_star[xindex], xcoord, ycoord, \
                                    T1_data[xindex], e_T1[xindex], \
                                    CT1_data[xindex], e_CT1[xindex]]])
                                break
                            else:
                            # A bin beyond this one exists (ie: star is NOT in
                            # the border of the y axis)
                                # Check if star is contained by top border in y
                                # axis.
                                if ycoord < yedges[ybin_index+1]:
                                    try:
                                    # Check if the bin exists.
                                        H_manual[xbin_index][ybin_index]
                                    except IndexError:
                                    # It doesn't, move on (see above)
                                        pass
                                    else:
                                    # It does, store star's data and increase
                                    # the count for this bin.
                                        H_manual[xbin_index][ybin_index][0] += 1
                                        H_manual[xbin_index][ybin_index].extend(\
                                        [[id_star[xindex], xcoord, ycoord,\
                                        T1_data[xindex], e_T1[xindex],\
                                        CT1_data[xindex], e_CT1[xindex]]])
                                    break
                else:
                # A bin beyond this one in the x axis exists so star is not in
                # the border.
                    # Check if star is contained by right border in x axis.
                    if xcoord < xedges[xbin_index+1]:
                        # Iterate through all edges in the y axis.
                        for ybin_index, yitem_edg in enumerate(yedges):

                            # Check if star falls inside this bin in the y axis.
                            if ycoord >= yitem_edg:
                                try:
                                    yedges[ybin_index+1]
                                except IndexError:
                                    # Star located in the border of the y axis.
                                    try:
                                    # Check if the bin exists.
                                        H_manual[xbin_index][ybin_index]
                                    except IndexError:
                                    # It doesn't, move on (see above)
                                        pass
                                    else:
                                        H_manual[xbin_index][ybin_index][0] += 1
                                        H_manual[xbin_index][ybin_index].extend(\
                                        [[id_star[xindex], xcoord, ycoord, \
                                        T1_data[xindex], e_T1[xindex], \
                                        CT1_data[xindex], e_CT1[xindex]]])
                                    break
                                else:
                                    if ycoord < yedges[ybin_index+1]:
                                        try:
                                            H_manual[xbin_index][ybin_index]
                                        except IndexError:
                                            pass
                                        else:
                                            H_manual[xbin_index][ybin_index][0] \
                                            += 1
                                            H_manual[xbin_index][ybin_index].\
                                            extend([[id_star[xindex], xcoord, \
                                            ycoord, T1_data[xindex], \
                                            e_T1[xindex], CT1_data[xindex], \
                                            e_CT1[xindex]]])
                                        break
    
    
    return H_manual
   
# Check to see if all items are equal. A couple of bins in the borders will
# probaly not have the same values.
#    for xindex, xelem in enumerate(H):
#        for yindex, yelem in enumerate(xelem):
#            if yelem != H_manual[xindex][yindex][0]:
#                print myfile, xindex, yindex, yelem, H_manual[xindex][yindex][0]
#              
#    print H[25][37], H_manual[25][37]
#
#    # Plot both 2D histograms to check that they are equal  
#    H_manual2 = []
#    for i in range(len(xedges)-1):
#        H_manual2.append([0 for _ in xrange(len(yedges)-1)])
#    for xindex, xelem in enumerate(H_manual):
#        for yindex, yelem in enumerate(xelem):
#            H_manual2[xindex][yindex] =  H_manual[xindex][yindex][0]
#    
#    fig = plt.figure(figsize=(10, 5)) # create the top-level container
#    gs = gridspec.GridSpec(1, 2)
#    plt.subplot(gs[0, 0])    
#    plt.imshow(H.transpose(), origin='lower')
#    plt.subplot(gs[0, 1])
#    plt.imshow(np.array(H_manual2).transpose(), origin='lower')
#    plt.show()
