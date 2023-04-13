import numpy as np
from scipy.stats import norm
from scipy.stats import entropy
import matplotlib.pyplot as plt

def get_bit_probs(T1,K_D,sigma,phi0_frac):
  """Comuptes probabilities of reordered samples, 
    cf. Eq (4) in "Modern random number generator design – Case study on a secured PLL-based TRNG"""
  i = np.arange(0,K_D) # ordered index from 0 to K_D-1
  Delta = T1/K_D
  phi0 = phi0_frac*T1 # initial_phase
  phi_i = np.remainder(phi0+i*Delta,T1) # signal phases at subsequent samples
  jitter_dist = norm(loc=phi_i,scale=sigma)
  part1 = jitter_dist.cdf(T1/2)-jitter_dist.cdf(0)
  part2 = jitter_dist.cdf(3*T1/2)-jitter_dist.cdf(T1)
  p = part1+part2
  return i,p

## Test 1: reproduce Fig 7. from "Modern random number generator design – Case study on a secured PLL-based TRNG"

i,ps = get_bit_probs(
  sigma = 9.6*1e-12,
  T1 = 1/( 634.7*1e6 ),
  K_D = 93,
  phi0_frac = 0.25,
)
plt.scatter(i,ps)

## Test 2: reproduce Tab. 4 (config 1) from "Modern random number generator design – Case study on a secured PLL-based TRNG"

_,ps = get_bit_probs(
  sigma =8.72*1e-12,
  T1 = 1/( 360.1*1e6 ),
  K_D = 279,
  phi0_frac = 0.25, # not sure if we shift the phase?
)

total_p = 1/2+1/2*np.prod(2*ps-1) # as per the formula of Davies
print(total_p,entropy([total_p,1-total_p],base=2))
