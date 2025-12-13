#coding:utf8

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
import scipy.stats

#https://docs.scipy.org/doc/scipy/reference/stats.html


dist_names = ['norm', 'beta', 'gamma', 'pareto', 't', 'lognorm', 'invgamma', 'invgauss',  'loggamma', 'alpha', 'chi', 'chi2', 'bradford', 'burr', 'burr12', 'cauchy', 'dweibull', 'erlang', 'expon', 'exponnorm', 'exponweib', 'exponpow', 'f', 'genpareto', 'gausshyper', 'gibrat', 'gompertz', 'gumbel_r', 'pareto', 'pearson3', 'powerlaw', 'triang', 'weibull_min', 'weibull_max', 'bernoulli', 'betabinom', 'betanbinom', 'binom', 'geom', 'hypergeom', 'logser', 'nbinom', 'poisson', 'poisson_binom', 'randint', 'zipf', 'zipfian']

print(dist_names)

# Etape 1 - Préparation et configuration

IMG_DIR = "img_seance4"
os.makedirs(IMG_DIR, exist_ok=True)

# Fonction utilitaire pour sauvegarder proprement les figures
def save_fig(fig, name):
    path = os.path.join(IMG_DIR, name)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)

# Etape 2 - Lois discrètes

# Loi de Dirac
def plot_dirac(k0=0, kmin=None, kmax=None, save="dirac.png"):
    if kmin is None: kmin = k0 - 5
    if kmax is None: kmax = k0 + 5
    k = np.arange(kmin, kmax + 1)
    pmf = (k == k0).astype(int)
    fig = plt.figure()
    plt.stem(k, pmf, use_line_collection=True)
    plt.title(f"Loi de Dirac (k0={k0})")
    plt.xlabel("k")
    plt.ylabel("p(k)")
    save_fig(fig, save)

# Loi uniforme discrète
def plot_uniform_discrete(a=0, b=10, save="uniform_discrete.png"):
    k = np.arange(a, b + 1)
    pmf = np.ones_like(k) / len(k)
    fig = plt.figure()
    plt.bar(k, pmf)
    plt.title(f"Uniforme discrète [{a}, {b}]")
    plt.xlabel("k")
    plt.ylabel("p(k)")
    save_fig(fig, save)

# Loi binomiale
def plot_binomiale(n=20, p=0.3, save="binomiale.png"):
    k = np.arange(0, n + 1)
    dist = scipy.stats.binom(n, p)
    fig = plt.figure()
    plt.bar(k, dist.pmf(k))
    plt.title(f"Binomiale (n={n}, p={p})")
    plt.xlabel("k")
    plt.ylabel("p(k)")
    save_fig(fig, save)

# Loi de Poisson
def plot_poisson(mu=3, save="poisson.png"):
    k = np.arange(0, 20)
    dist = scipy.stats.poisson(mu)
    fig = plt.figure()
    plt.bar(k, dist.pmf(k))
    plt.title(f"Poisson (λ={mu})")
    plt.xlabel("k")
    plt.ylabel("p(k)")
    save_fig(fig, save)

# Loi de Zipf-Mandelbrot
def zipf_mandelbrot_pmf(s=1.5, q=1.0, kmax=100):
    k = np.arange(1, kmax + 1)
    probs = (k + q) ** (-s)
    probs /= probs.sum()
    return k, probs

def plot_zipf_mandelbrot(s=1.5, q=1.0, kmax=100, save="zipf_mandelbrot.png"):
    k, pmf = zipf_mandelbrot_pmf(s, q, kmax)
    fig = plt.figure()
    plt.bar(k, pmf)
    plt.title(f"Zipf-Mandelbrot (s={s}, q={q})")
    plt.xlabel("k")
    plt.ylabel("p(k)")
    save_fig(fig, save)

# Etape 3 - Lois continues

def plot_pdf(frozen, x, title, save):
    fig = plt.figure()
    plt.plot(x, frozen.pdf(x))
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    save_fig(fig, save)

# Lois continues principales
def plot_continues():
    # Poisson (en PMF, même si discrète)
    plot_poisson(3, save="poisson_continu.png")

    # Loi normale
    x = np.linspace(-5, 5, 400)
    plot_pdf(scipy.stats.norm(0, 1), x, "Normale N(0,1)", "normale.png")

    # Loi log-normale
    x = np.linspace(0.01, 10, 400)
    plot_pdf(scipy.stats.lognorm(s=0.6), x, "Log-normale", "lognormale.png")

    # Loi uniforme continue
    x = np.linspace(0, 1, 200)
    plot_pdf(scipy.stats.uniform(0, 1), x, "Uniforme continue [0,1]", "uniforme_continue.png")

    # Loi du chi²
    x = np.linspace(0, 20, 400)
    plot_pdf(scipy.stats.chi2(4), x, "Chi² (df=4)", "chi2.png")

    # Loi de Pareto
    x = np.linspace(1, 10, 400)
    plot_pdf(scipy.stats.pareto(2.5), x, "Pareto (b=2.5)", "pareto.png")

# Etape 4 - Fonctions moyenne et écart-type

def mean_std_from_frozen(dist):
    return float(dist.mean()), float(dist.std())

def mean_std_from_pmf(k, pmf):
    m = (k * pmf).sum()
    v = ((k - m) ** 2 * pmf).sum()
    return float(m), float(np.sqrt(v))

# Etape 5 - Exécution principale
if __name__ == '__main__':

    # Lois discrètes
    plot_dirac()
    plot_uniform_discrete()
    plot_binomiale()
    plot_poisson()
    plot_zipf_mandelbrot()

    # Lois continues
    plot_continues()

    # Calculs de moyenne / écart-type exemples
    print("\n--- Moyennes et écarts-types ---\n")
    print("Dirac(0) :", mean_std_from_pmf(np.array([0]), np.array([1])))
    print("Uniforme discrète 0..10 :", mean_std_from_pmf(np.arange(0,11), np.ones(11)/11))
    print("Binomiale(20,0.3) :", mean_std_from_frozen(scipy.stats.binom(20,0.3)))
    print("Poisson(3) :", mean_std_from_frozen(scipy.stats.poisson(3)))
    k, pmf = zipf_mandelbrot_pmf()
    print("Zipf-Mandelbrot :", mean_std_from_pmf(k, pmf))
    print("Normale(0,1) :", mean_std_from_frozen(scipy.stats.norm(0,1)))
    print("Log-normale :", mean_std_from_frozen(scipy.stats.lognorm(0.6)))
    print("Pareto(2.5) :", mean_std_from_frozen(scipy.stats.pareto(2.5)))

    print(f"\nImages sauvegardées dans '{IMG_DIR}'")

