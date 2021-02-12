import unittest
from testbandit import experiment

Variation = experiment.Variation
Experiment = experiment.Experiment

class TestVariation( unittest.TestCase ):

    def test_init( self ):
        variation = Variation( 'Variation A', 10, 22, .04 )
        self.assertEqual( 'Variation A', variation.name() )
        self.assertEqual( 10, variation.prior_a() )
        self.assertEqual( 22, variation.prior_b() )
        self.assertEqual( 0, variation.posterior_a() )
        self.assertEqual( 0, variation.posterior_b() )
        self.assertEqual( None, variation.value_at_risk() )
        self.assertEqual( None, variation.maximum_likelihood_estimate() )
        self.assertEqual( None, variation.posterior_mean() )
        self.assertEqual( None, variation.credible_interval() )
        self.assertEqual( None, variation.sample_from_posterior( 1 ) )

    def test_add_trials_successes_greater_than_trials( self ):
        variation = Variation( 'Variation A', 1, 1, .04 )
        with self.assertRaises( ValueError ):
            variation.add_trials( 1, 0 )

    def test_add_trials_single_success( self ):
        variation = Variation( 'Variation A', 11, 23, .45 )
        variation.add_trials( 1, 1 )
        self.assertEqual( 11, variation.prior_a() )
        self.assertEqual( 23, variation.prior_b() )
        self.assertEqual( 12, variation.posterior_a() )
        self.assertEqual( 23, variation.posterior_b() )
        self.assertAlmostEqual( 0.905, variation.value_at_risk(), 2 )

        # Prior data doesn't play into the MLE, so 1 trial 1 success is MLE of
        #   100% for the observed data
        self.assertEqual( 1, variation.maximum_likelihood_estimate() )

        self.assertAlmostEqual( 0.34285714285714286, variation.posterior_mean() )
        self.assertAlmostEqual( 0.19745864791234233, variation.credible_interval()[ 0 ] )
        self.assertAlmostEqual( 0.5052653008985046, variation.credible_interval()[ 1 ] )

    def test_sample_from_posterior_1_time( self ):
        variation = Variation( 'Variation A', 11, 23, .45 )
        variation.add_trials( 1, 1 )
        samples = variation.sample_from_posterior( 1 )
        self.assertEqual( len( samples ), 1 )
        self.assertGreater( samples[ 0 ], 0 )
        self.assertLess( samples[ 0 ], 1 )

    def test_sample_from_posterior_10_times( self ):
        variation = Variation( 'Variation A', 11, 23, .45 )
        variation.add_trials( 1, 1 )
        samples = variation.sample_from_posterior( 10 )
        self.assertEqual( len( samples ), 10 )
        for sample in samples:
            self.assertGreater( sample, 0 )
            self.assertLess( sample, 1 )


class TestExperiment( unittest.TestCase ):

    def test_add_variation_1( self ):
        variation = Variation( 'Variation A', 0, 0, 0 )
        experiment = Experiment()
        experiment.add_variation( variation )

        self.assertEqual( 1, len( experiment.get_variations() ) )
        self.assertEqual( variation, experiment.get_variations()[ 0 ] )

    def test_add_variation_3( self ):
        variation1 = Variation( 'Variation A', 0, 0, 0 )
        variation2 = Variation( 'Variation B', 0, 0, 0 )
        variation3 = Variation( 'Variation C', 0, 0, 0 )

        experiment = Experiment()

        experiment.add_variation( variation1 )
        experiment.add_variation( variation2 )
        experiment.add_variation( variation3 )

        variations = experiment.get_variations()
        self.assertEqual( 3, len( variations ) )
        self.assertEqual( variation1, variations[ 0 ] )
        self.assertEqual( variation2, variations[ 1 ] )
        self.assertEqual( variation3, variations[ 2 ] )

    def test_winning_variation( self ):
        variation1 = Variation( 'Variation A', 1, 1, 0 )
        variation2 = Variation( 'Variation B', 1, 1, 0 )
        variation3 = Variation( 'Variation C', 1, 1, 0 )

        experiment = Experiment()

        experiment.add_variation( variation1 )
        experiment.add_variation( variation2 )
        experiment.add_variation( variation3 )

        variation1.add_trials( 50, 100 )
        variation2.add_trials( 60, 100 )
        variation3.add_trials( 40, 100 )

        experiment.calculate_winning_variation()
        self.assertEqual( variation2, experiment.get_winning_variation() )

        winning_percentages = experiment.get_winning_percentages()
        self.assertAlmostEqual( 0.078025, winning_percentages[ 0 ], 2 )
        self.assertAlmostEqual( 0.920655, winning_percentages[ 1 ], 2 )
        self.assertAlmostEqual( 0.001320, winning_percentages[ 2 ], 2 )

    def test_thompson_sample( self ):
        variation1 = Variation( 'Variation A', 1, 1, 0 )
        variation2 = Variation( 'Variation B', 1, 1, 0 )
        variation3 = Variation( 'Variation C', 1, 1, 0 )

        experiment = Experiment()

        experiment.add_variation( variation1 )
        experiment.add_variation( variation2 )
        experiment.add_variation( variation3 )

        # So that the test doesn't fail intermitently, we set variation 1 & 3 to 0
        variation1.add_trials( 0, 100 )
        variation2.add_trials( 99, 100 )
        variation3.add_trials( 0, 100 )

        sampled_variation = experiment.thompson_sample( 3 )
        self.assertEqual( variation2, sampled_variation )

if __name__ == '__main__':
    unittest.main()
