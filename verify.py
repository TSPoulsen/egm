import numpy as np
from chi2comb import chi2comb_cdf, ChiSquared
import matplotlib.pyplot as plt
from scipy.stats import zipfian

"""
This script was used purely for visual verification of the chi2comb package
"""

sample_size = 10**4
dims = 100 
sig_total = 10
scew = 10


def verify(sigmas: np.ndarray):
    means = np.zeros((dims))
    sample = np.random.normal(means, sigmas, size=(sample_size, dims))
    ips = np.sum(sample * sample, axis=1)
    xs = np.arange(0,np.max(ips),0.1)
    chi2s =         [ChiSquared(sigmas[i]**2, 0, 1) for i in range(dims)]
    theory_ips2 = np.array([chi2comb_cdf(x,chi2s,0, lim = 50000)[0] for x in xs])
    plt.plot(xs, theory_ips2, color = "r", label="chi2comb")
    plt.hist(
        ips,
        bins = 100,
        cumulative=True,
        density=True,
        label="Emperical Data",
        histtype="step",
        alpha=0.8,
        color="k",
    )
    plt.xlabel("Squared norm $\|x \|^2$")
    plt.ylabel("Cumulative Distribution")
    plt.legend()
    plt.show()


xs = np.arange(1,dims+1,1).astype("int16", copy=False)
sigmas = zipfian.pmf(xs, scew, dims) * sig_total
sig_sum = np.sum(sigmas)
sig_trans = np.sqrt(sigmas / sig_sum)

verify(sigmas)
verify(sig_trans)