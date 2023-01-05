from scipy.stats import zipfian
import matplotlib.pyplot as plt
import numpy as np
import functools
import itertools
import argparse
from chi2comb import chi2comb_cdf, ChiSquared
import pandas as pd
from tqdm import tqdm

from typing import Dict

#TODO: Ensure that cdf follows actual distribution


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", type=int, nargs="+", default=[100])
    parser.add_argument("-n_pow", type=int, nargs="+", default=[10e6])
    parser.add_argument("--scew","-a",  nargs="+", type=float, default=[1.0])
    parser.add_argument("--sigma-total", nargs="+", type=int, default=[1])
    return parser.parse_args()


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

def calc_err(dims: int, n_pow: int, scew: float, sig_total: int) -> Dict:
    xs = np.arange(1,dims+1,1).astype("int16", copy=False)
    sigmas = zipfian.pmf(xs, scew, dims) * sig_total
    sig_sum = np.sum(sigmas)
    variance_trans = sigmas / sig_sum

    chi2s =         [ChiSquared(sigmas[i]**2, 0, 1) for i in range(dims)]
    chi2s_trans =   [ChiSquared(variance_trans[i], 0, 1) for i in range(dims)]

    partial_cdf_normal = functools.partial(chi2comb_cdf, chi2s=chi2s, gcoef=0, atol=10**(-n_pow))
    cdf_normal = lambda q: partial_cdf_normal(q)[0:2]

    partial_cdf_trans = functools.partial(chi2comb_cdf, chi2s=chi2s_trans, gcoef=0, atol=10**(-n_pow))
    cdf_trans = lambda q: partial_cdf_trans(q)[0:2]

    cutting_prob = 10**(-n_pow)
    c_normal = bs_icdf(cdf_normal,1 - cutting_prob, tol = 10**(-n_pow-1))
    c_trans = bs_icdf(cdf_trans,1 - cutting_prob, tol = 10**(-n_pow-1))

    normal_err = 4*c_normal*dims
    invb_sq = [(sigmas[i]*sig_sum) for i in range(dims)]
    trans_err = 4 * c_trans * sum(invb_sq)
    return {"trans_err": trans_err, "normal_err": normal_err, "c_normal": c_normal, "c_trans": c_trans}


def save_ans(ans: Dict, df: pd.DataFrame):
    mask = (df["d"] == ans["d"]) & (df["n_pow"] == ans["n_pow"]) & (df["scew"] == ans["scew"]) & (df["sigma_total"] == ans["sigma_total"])
    h = df.loc[mask]
    if len(h) == 0:
        df = df.append(ans, ignore_index=True)
    else: print("Result found:",ans)
    return df


if __name__ == "__main__":
    args = get_args()

    results = pd.read_csv("results.csv",delimiter=",",index_col=False, header=0)
    all_combs = list(itertools.product(args.d, args.n_pow, args.scew, args.sigma_total, repeat=1))
    for d, n_pow, scew, sig_tot in tqdm(all_combs):
        ans = calc_err(d, n_pow, scew, sig_tot)
        ans["d"] = d
        ans["n_pow"] = n_pow
        ans["scew"] = scew
        ans["sigma_total"] = sig_tot 
        results = save_ans(ans, results)
    results.to_csv("results.csv",index=False)
