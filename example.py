from testbandit import experiment
from scipy.stats import beta
import numpy as np
import matplotlib.pyplot as plt

def plot_beta( a, b ):
    x = np.arange (0.0, 1, 0.001)
    y = beta.pdf(x, a=a, b=b)
    plt.plot(x,y)
    plt.show()

def print_summary( variation ):
    print( "----", variation.name(), "----")
    print( "Prior alpha:", variation.prior_a() )
    print( "Prior beta:", variation.prior_b() )
    print( "Posterior alpha:", variation.posterior_a() )
    print( "Posterior beta:", variation.posterior_b() )
    print( "Posterior Mean: %2.3f" % variation.posterior_mean() )
    print( "Maximum Likelihood Estimate: %2.3f" % variation.maximum_likelihood_estimate() )
    print( "Probability that conversion rate is less than %2.3f" % variation.value_at_risk_threshold(), "-", variation.value_at_risk() )

    ( lower, upper ) = variation.credible_interval()

    print()
    print( "Equal tail 95% credible interval" )
    print( "Lower bound: %2.3f" % lower )
    print( "Upper bound: %2.3f" % upper )

Variation = experiment.Variation
Experiment = experiment.Experiment

# The Value at Risk is a threshold that we want to make sure we don't go below. We can analyze any
#   varation and see what the probability is that the variation would convert lower than our Value 
#   at Risk.
value_at_risk = .58

# Create some variations
variation_a = Variation( 'Variation A', 1, 1, value_at_risk )
variation_b = Variation( 'Variation B', 1, 1, value_at_risk )
variation_c = Variation( 'Variation C', 1, 1, value_at_risk )

# Create an experiment and add the variations
experiment = Experiment()
experiment.add_variation( variation_a )
experiment.add_variation( variation_b )
experiment.add_variation( variation_c )

# Capture some trials (obviously Variation B is the best performing)
# add_trials( successes, trials )
print( "-=-=-=-=-=-=" )
print( "Adding trials:" )
print( "A: 5 out of 10" )
print( "A: 6 out of 10" )
print( "A: 4 out of 10" )
variation_a.add_trials( 5, 10 )
variation_b.add_trials( 6, 10 )
variation_c.add_trials( 4, 10 )

experiment.calculate_winning_variation()
winning_variation = experiment.get_winning_variation()
winning_percentages = experiment.get_winning_percentages()

print( "-=-=-=-=-=-=" )
print( "Winning variation with the given data (200,000 samples): ", winning_variation.name() )
print( "Probability of being the winning variation [A, B, C]: ", winning_percentages )

# For a bandit test, you want to use Thompson Sampling. Basically, you draw a sample
#   from each variation's posterior distribution and get the variation that produced
#   the sample with the highest conversion rate.
sampled_variation = experiment.thompson_sample()
print( "-=-=-=-=-=-=" )
print( "Next variation to serve (single sample using Thompson Sampling):", sampled_variation.name() )

# Capture some more trials (obviously Variation B is the best performing at this point). The great thing
#   about the Bayesian approach is that you can sequentially add trial data as you get it, or add it all
#   in at once. The Bayesian approach doesn't suffer from the "peeking" problems that you have when using
#   the Frequentist model.
print( "-=-=-=-=-=-=" )
print( "Adding trials:" )
print( "A: 52 out of 100" )
print( "A: 64 out of 100" )
print( "A: 43 out of 100" )
variation_a.add_trials( 52, 100 )
variation_b.add_trials( 64, 100 )
variation_c.add_trials( 43, 100 )

# For a bandit test, you want to use Thompson Sampling. Basically, you draw a sample
#   from each variation's posterior distribution and get the variation that produced
#   the sample with the highest conversion rate.
experiment.calculate_winning_variation()
winning_variation = experiment.get_winning_variation()
winning_percentages = experiment.get_winning_percentages()

print( "-=-=-=-=-=-=" )
print( "Winning variation with the given data (200,000 samples): ", winning_variation.name() )
print( "Probability of being the winning variation [A, B, C]: ", winning_percentages )

print( "-=-=-=-=-=-=" )
print( "Let's look at the details of the winner" )
print_summary( winning_variation )

print( "-=-=-=-=-=-=" )
print( "Let's plot the posterior distribution for the winner" )
plot_beta( winning_variation.posterior_a(), winning_variation.posterior_b() )
