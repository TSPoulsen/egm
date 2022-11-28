## Der skal formuleres
- Projekt Titel
- Projekt beskrivelse (ikke en problemformulering, selvom denne nok vil være den mest beskrivende)
    - Der er altså ingen binding til problemformulering

## Aftalt med vejleder
- Hvor ofte vi skal mødes (hvor lange disse møder skal være) 
    - Vi har vel 8-9 uger
    - Hvor mange timer der vejledes
- Hvad der forventes af vejleder til disse møder
- Hvad der forventes af mig til disse møder
- Kommunikationsform - altså uden for møder (mail/teams etc.)


## Andet praktisk
- Jeg skriver på engelsk
- 7.5 etcs (10 etcs hvis det er nødvendigt for at lave noget jeg gerne vil)

- Når aftalerne er på plads laver jeg en kontrakt som vi underskriver og jeg indsender den til uddannelse@diku.dk, som efterfølgende vil indhente den endelige godkendelse fra studielederen.


## Review and noise investigation of the Elliptical Gaussian Mechanism


The report will consist of two parts
1. A review of the differentially private algorithm 'Elliptical Gaussian Mechanism' created by Rasmus Pagh and Christian (I don't know his surname) and theoretical results of the mechanism.
2. An investigation of the noise introduced by the algorithm. This is done either by creating synthetic datasets and then analysing the norm of the noise, or through a theoretic investigation of norm of the noise.

#### Second edition:
The report will consist of two parts:

A review of central termonology and theorems in differential privacy, then followed by covering aspects of the article 'Private Vector Aggregation when Coordinates have Different Sensitivity" written by Rasmus Pagh and Christian Lebeda.
I will be focusing on the 'Elliptical Gaussian Mechanism' (EGM) and when covering termonology and theorems from differential privacy I will specifically focus on those which relate to the EGM.

As the EGM expects data to lie within pre-specified bounds I will in the second part of the project investigate how to apply the EGM when data is assumed to come from a multivariate normal distribution instead. This investigation can include:
- Details on how privacy can be preserved
- Giving bounds for the expected l2-error
- An emperical evaulation of the method in this setting


### Meeting plans
- Info/book about generalized chi square
- I need not introduce the Gaussian distribution, but perhaps some results which are of importance to the project


### TODO:
- Make argument for why clipping data preserves privacy. Should be closely related to definition of ($\epsilon$,$\delta$)-DP.
- Think about transforming data such that expected norm is $1$ (in theory anything such that anything outside this is clipped). This is related to generalized chi square distributions.

Let $x$ be multivariate normally distributed,
then
$$ <x,x> = x^Tx = \| x\|^2$$
$$ E[\| x \|^2] = tr[\Sigma] + \| \mu \|^2 $$
$$ var[\| x \|^2] = 2 tr[\Sigma \Sigma] + 4\mu^T\Sigma\mu$$ 

I can always transform a normal random variable to standard normal variable by
$$ X \sim N(\mu,\sigma^2)$$
$$\frac{X-\mu}{\sigma} \sim N(0,1)$$
Generalized Chi square is defined as the linear sum of indpendent noncentral chi-square variables
$$ \xi = \sum_{i} w_i x_i $$ 
where each $x_i \sim \sum_{j} X_j^2$, and $X_j \sim N(\mu_j,1)$

so in my case $j=1$ and 
$$ \xi = \sum_i w_i X_i^2$$
Is it hen correct to set $w_i = \sigma_i^2$, as $\sigma_i X_i \sim N(\mu_i, \sigma_i^2)$

