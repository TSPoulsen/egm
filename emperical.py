from scipy.stats import zipfian
import matplotlib.pyplot as plt
import numpy as np
import functools
from chi2comb import chi2comb_cdf, ChiSquared

#TODO: Ensure that cdf follows actual distribution

def transform(sigmas: np.ndarray):
    bj = np.sqrt(np.sum(sigmas))
    return np.sqrt(sigmas) / bj

def bs_icdf(cdf, prob, tol):
    lb, ub = 0, 1
    while True:
        p, code = cdf(ub)
        if code == 0 and p < prob:
            lb = ub
            ub *= 2
        elif code == 0 and p >= prob:
            break
        else:
            ub += 10

    p = 0
    while lb < ub and abs(p - prob) > tol:
        mid = (lb + ub)/2
        p, code = cdf(mid)
        while code != 0:
            mid += 1
            p, code = cdf(mid)
        if p < prob:
            lb = mid
        else:
            ub = mid
    return (ub + lb)/2

d = 100
n_pow = 6
a = 1 # parameter for zipf distribution
total = d 

xs = np.arange(1,d+1,1).astype(int)

sigmas = zipfian.pmf(xs, a, d) * 10 
sigmas_trans = transform(sigmas)

chi2s = [ChiSquared(sigmas[i]**2, 0, 1) for i in range(d)]
chi2s_trans = [ChiSquared(sigmas_trans[i]**2, 0, 1) for i in range(d)]

#chi2comb_cdf(x,chi2s,0, lim = 50000)
partial_cdf_normal = functools.partial(chi2comb_cdf, chi2s=chi2s, gcoef=0, atol=10**(-n_pow))
cdf_normal = lambda q: partial_cdf_normal(q)[0:2]

partial_cdf_trans = functools.partial(chi2comb_cdf, chi2s=chi2s_trans, gcoef=0, atol=10**(-n_pow))
cdf_trans = lambda q: partial_cdf_trans(q)[0:2]

cutting_prob = 10**(-n_pow)
c_normal = bs_icdf(cdf_normal,1 - cutting_prob, tol = 10**(-n_pow-1))
c_trans = bs_icdf(cdf_trans,1 - cutting_prob, tol = 10**(-n_pow-1))
print(c_normal, c_trans)

normal_err = 4*c_normal*d
sigsum = np.sum(sigmas)
#print(sigmas)
bjs = [1/(sigmas[i]*sigsum) for i in range(d)]
print(sum(bjs))
#print(bjs)
trans_err = 4 * c_trans * sum(bjs)
print(trans_err, normal_err)

#plt.vlines(xs, 0, sigmas)
#plt.show()
