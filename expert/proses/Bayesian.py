import numpy as np

class Bayesian:
    def __init__(self, priors):
        self.priors = priors

    
    def posterior(self, likelyhood):
        evidence_prior = sum(self.priors[h] * likelyhood[h] for h in self.priors)
        posteriors = {h:(self.priors[h] * likelyhood[h]) / evidence_prior for h in self.priors}

        return posteriors
    
    def posteriors_multiple(self, evidence):
        numerator = {}
        for h in self.priors:
            prob = self.priors[h]
            for ev in evidence:
                prob *= ev[h]
            numerator[h] = prob
        total = sum(numerator.values())
        prosterior = {h: numerator[h]/total for h in numerator}
        return prosterior
    
    def __str__(self):
        return f'bayesian(prior = {self.priors})'
    
# for testing!!!
# prior = {'flu' : 0.25, 'covid' : 0.15, 'alergi_dingin':0.15}
# caught = {'flu' : 0.1, 'covid' : 0.8, 'alergi_dingin': 0.1}
# bayes = Bayesian(prior)
# print(f' batuk {bayes.posterior(caught)}')

# headache = {'flu' : 0.5, 'covid' : 0.5, 'alergi_dingin' : 0.5}
# print(f' sakit kepala {bayes.posterior(headache)}')

# print(f' multiply {bayes.posteriors_multiple([caught, headache])}')
    