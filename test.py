from scipy.stats import chi2
import matplotlib.pyplot as plt

dof = range(1,5)

# Perform experiement where each Gaussian is not N(0,I), but instead N(0, \sigma * I), same variance for each but it is optimal
# Look into stats.wishart or python package "chi2comb 0.1.0"

probs = []
for degree in dof:
    probs.append( 1-chi2(degree).cdf(1) ) 
plt.plot(dof,probs)
plt.show()



