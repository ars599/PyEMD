"""
org: matlabe version from https://github.com/leeneil
convert to python
owned by Arnold Sullivan
history 02 10 2017
Oceans and Atmosphere CSIRO
web: arnold.sullivan@csiro.au

"""

def eemd2d(img,goal, nos_wn):
    # 2-D EEMD, an implenmation of HHT
    # written by Neil Po-Nan Li @ Inst. of Physics, Academia Sinica, Taiwan
    # v1.  2012/10/6
    # v2.  2014/3/10 bug fixes
    # v2.1 2014/3/17 stablity issue fixed

    import numpy as np
    from PyEMD import EEMD

    sz = np.shape(img)
    n1 = sz[0]
    n2 = sz[1]
    nimf = goal
    eemd = EEMD()
    eemd.trials = goal
    eemd.noise_width = nos_wn
    emd = eemd.EMD
    emd.extrema_detection="parabol"

    std_img = np.std(img)
    img = img / std_img

#% 2-D EEMD   dim#1
    G    = np.zeros([n1, n2, nimf+1])
    for u in range(0,n1-1):
      row_modes = eemd(img[u, :],max_imf=goal)
      if not row_modes.all: print("error in dim 1")
      row_modes[np.isnan(row_modes)] = 0
      tz = np.shape(row_modes)
      nf = tz[0]
      G[u,:,0:nf] = np.transpose(row_modes)

#    G = Gtmp[:,:,0:nimf]
#% 2-D EEMD    dim#2
    D    = np.zeros([n1, n2, nimf+1, nimf+1])
    for m in range(0,nimf):
        print('Solving mode ', m+1, '/', nimf)
        # solve and store
        for v in range(0,n2-1):
           col_modes = eemd(G[:, v, m],max_imf=goal)
           if not col_modes.all: print("error in dim 2")
           col_modes[np.isnan(col_modes)] = 0
           tz = np.shape(col_modes)
           nf = tz[0]
           D[:,v,m,0:nf] = np.transpose(col_modes) 

#    D = Dtmp[:,:,0:nimf,0:nimf]
#% Combine modes
    H = np.zeros([n1, n2, nimf])
    for m in range(0,nimf):
        for k in range(m,nimf):
            H[:, :, m] = H[:, :, m] + D[:, :, m, k]
            H[:, :, m] = H[:, :, m] + D[:, :, k, m]
        H[:, :, m] =     H[:, :, m] - D[:, :, m, m]

# for m = (goal+1):-1:1
#     H(:,:,m) = sum( sum( D(:,:,m:end,m:end), 4), 3);
#     if m < (goal+1)
#         H(:,:,m) = H(:,:,m) - sum( H(:,:, (m+1):end ), 3);
#     end
# end
    modes = H * std_img

#    return modes
    return G, D, H


