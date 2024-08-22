import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pathlib
from tqdm import tqdm
import ot
from scipy.spatial.distance import pdist, squareform
from sklearn import manifold
import warnings
warnings.filterwarnings("ignore")

##### Helper functions
def calculate_barycenter(A, n = 300, show_plot=False):
    n_distributions = A.shape[1]

    # loss matrix + normalization
    M = ot.utils.dist0(n)
    M /= M.max()

    weights = [1/n_distributions for item in range(n_distributions)]
    x = np.arange(n, dtype=np.float64)
    # l2bary
    bary_l2 = A.dot(weights)

    # wasserstein
    reg = 1e-3
    bary_wass = ot.bregman.barycenter(A, M, reg, weights)
    if show_plot:
        f, (ax1, ax2) = plt.subplots(2, 1, tight_layout=True, num=1)
        ax1.plot(x, A, color="black")
        ax1.set_title('Distributions')

        ax2.plot(x, bary_l2, 'r', label='l2')
        ax2.plot(x, bary_wass, 'g', label='Wasserstein')
        ax2.set_title('Barycenters')

        plt.legend()
        plt.show()
    return bary_l2

def calculate_ot_distance_to_ref(input_sample, bary_l2, inputdf, n = 300):
    x = np.arange(n, dtype=np.float64)
    M = ot.dist(x.reshape((n, 1)), x.reshape((n, 1)), 'euclidean')
    M /= M.max() * 0.1
    a = inputdf[input_sample].values
    a = np.array(a)
    b = bary_l2
    d_emd = ot.emd2(a, b, M)  # direct computation of OT loss
    return d_emd

def ot_distance(a, b, n = 300):
    x = np.arange(n, dtype=np.float64)
    M = ot.dist(x.reshape((n, 1)), x.reshape((n, 1)), 'euclidean')
    M /= M.max() * 0.1
    
    d_emd = ot.emd2(a, b, M)  # direct computation of OT loss
    return d_emd

def ot_distance_nuc(a, b, n = 601):
    x = np.arange(n, dtype=np.float64)
    M = ot.dist(x.reshape((n, 1)), x.reshape((n, 1)), 'euclidean')
    M /= M.max() * 0.1
    
    d_emd = ot.emd2(a, b, M)  # direct computation of OT loss
    return d_emd

def ot_distance_em(a, b, n = 256):
    x = np.arange(n, dtype=np.float64)
    M = ot.dist(x.reshape((n, 1)), x.reshape((n, 1)), 'euclidean')
    M /= M.max() * 0.1
    
    d_emd = ot.emd2(a, b, M)  # direct computation of OT loss
    return d_emd