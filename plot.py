import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict
import numpy as np
from scipy.stats import zipfian

# More scew/sigma_total leads to more error for normal but not for transformed
# Generally more error when total sigma is greater
# More scew better transform


def generate_plot(df, xlab, ylab, name):

    fig, axs = plt.subplots(1,2)
    print(f"Generating {name}.png")
    location = f"plots/{name}.png" 
    start, end = np.min(df["normal_err"]), np.max(df["normal_err"])
    a = 990/(end - start)
    b = 10 - a*start
    for ax, err in zip(axs,["normal_err","trans_err"]):
        sizes = a*df[err] + b
        ax.scatter(df[xlab], df[ylab], s=sizes)
        ax.set_xlabel(xlab)
        ax.set_ylabel(ylab)
        ax.set_xscale("log")
        ax.set_yscale("log")
    fig.savefig(location)
    plt.close(fig)

def gen_all_plots(cols, blacklist: Dict) -> None:
    df = pd.read_csv("results.csv")
    for i,col1 in enumerate(cols):
        for col2 in cols[i+1:]:
            if col1 == col2: continue
            for val1 in df[col1].unique():
                if val1 in blacklist[col1]: continue
                for val2 in df[col2].unique():
                    if val2 in blacklist[col2]: continue
                    sub_df = df[df[col1] == val1]
                    sub_df = sub_df[sub_df[col2] == val2]
                    left = list(set(cols).difference(set([col1,col2])))
                    assert len(left) == 2, f"{left}"
                    generate_plot(sub_df, left[0], left[1], name=f"{col1}{val1}__{col2}{val2}")

def generate_improve_box():
    df = pd.read_csv("results.csv")
    data = []
    for scew in df["scew"].unique():
        sub_df = df[df["scew"] == scew]
        d = sub_df["normal_err"] / sub_df["trans_err"]
        data.append( (scew, d) ) 
    data.sort(key=lambda x: x[0])
    fig, axs = plt.subplots(1,2)
    bp = axs[0].boxplot([d for _, d in data[:2]])
    bp = axs[1].boxplot([d for _, d in data[2:]])
    axs[1].set_yscale("log")
    plt.show()

def generate_improve_plot(n_pows):
    df = pd.read_csv("results.csv")
    df = df[df["sigma_total"] == 1]

    fig, axs = plt.subplots(1,3, sharey=True, figsize=(15,7))
    for i, d in enumerate([10,100,1000]):
        d_df = df[df["d"] == d]
        for n_pow in n_pows:
            sub_df = d_df[d_df["n_pow"] == n_pow]
            sub_df = sub_df.sort_values(by="scew")
            ratio = sub_df["normal_err"] / sub_df["trans_err"]
            axs[i].plot(sub_df["scew"], ratio, label=r"$n=10^{" + str(n_pow) + r"}$")

        axs[i].set_title(r"$d=10^{" + str(i+1) + r"}$")
        axs[i].set_xscale("log")
        axs[i].set_yscale("log")
        axs[i].set_xlabel(r"Skew ($\alpha$)")
        #axs[i].vlines(1.0,0,2000, linestyles="dashed")
        axs[i].grid()

        axs[i].set_ylim(1,2000)

    fig.tight_layout(pad=1)
    axs[0].set_ylabel(r"Improvement $\left( \frac{E_n}{E_t} \right)$", fontsize=16)
    axs[0].legend(loc="upper left")
    fig.savefig("result.png", bbox_inches='tight')
    #plt.show()

def generate_skew_plot(scew):
    dims = 100
    fig, axs = plt.subplots(1,3, figsize=(15,3))
    for i, scew in enumerate([0.1, 1, 3]):
        xs = np.arange(1,dims+1,1).astype("int16", copy=False)
        sigmas = zipfian.pmf(xs, scew, dims)
        axs[i].bar(xs,sigmas, width=0.7)
        axs[i].set_title(r"$\alpha = " + str(scew) + r"$")
        axs[i].set_xlabel(r"Index $i$ of $\sigma_i$")
    axs[0].set_ylabel(r"Contribution of $\sigma_i$", fontsize=10)
    plt.savefig("scew_dist.png", bbox_inches="tight")
"""
blacklist = {   "d":[250],
                "n_pow":[2,4,5],
                "sigma_total":[10,100],
                "scew":[0.1]}
#gen_all_plots(list(blacklist.keys()), blacklist)

#generate_improve()
"""
#generate_improve_plot(n_pows=[2,3,6])
generate_skew_plot(0.1)