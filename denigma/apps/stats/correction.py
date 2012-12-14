"""p-value Corrections for multiple testing.
Equivalent of the R's p/adjust"""

def bonferroni_adjustment(pvalues):
    """Correct a list of p-values using the Bonferroni adjustment
    Return a list of corrected p-values; null values are ignored.
    cf. http://en.wikipedia.org/wiki/Bonferroni_correction """
    n = len(filter(lambda x: x != None, pvalues)) + 0.0

    adjusted_pvalues = []
    for pvalue in pvalues:
        if not pvalue:
            adjusted_pvalues.append(None)
        else:
            adjusted_pvalues.append(min(pvalue * n, 1))

    return adjusted_pvalues

def holm_adjustment(pvalues):
    """Correct a list of p-values using the Holm-Bonferri adjustment.
    Return a list of corrected p-values; null values are ignored.
    cf. http://en.wikipedia.org/wiki/Holm-Bonferroni_method """
    # Multiply p-values by a corrective factor, ignore null entries:
    n, c = len(filter(lambda x: x != None, pvalues)), 0
    m = []

    adjusted_and_ranked_pvalues = []
    for i, (i_, pvalue) in enumerate(sorted(enumerate(pvalues), lambda x, y: cmp(x[1], y[1]))):
        m.append(i_)
        if not pvalue:
            adjust_and_ranked_pvalues.append(None)
        else:
            adjusted_and_ranked_pvalues.append(min(pvalue * (n - c), 1))
            c += 1

    # Corrent the p-values out of their proper order:
    adjusted_pvalues = [0 for c in range(i+1)]
    for i, pvalue in enumerate(adjusted_and_ranked_pvalues):
        if pvalue:
            adjusted_and_ranked_pvalues[i] = max(filter(lambda x: x != None, adjusted_and_ranked_pvalues[:i+1]))
##        else:
        adjusted_pvalues[m[i]] = adjusted_and_ranked_pvalues[i]

    return adjusted_pvalues

def fdr(pvalues, produce_ranking=False):
    """Given a lit of p-values, produce a ranked list of increasing q-values.
    A q-value in position k represents the false discovery rate, or expected
    propoertion of false positives in the k first hypotheses.
    Assumes that the tets are independent or postively correlated.

    Uses the Bejamini-Hochberg algorthim
    cf.  http://en.wikipedia.org/wiki/False_discovery_rate """
    # Multiply p-values by  a corrective factor, ignore null entries
    n, c = len(filter(lambda x: x != None, pvalues)), 0
    m = []

    qvalues = []
    for i, (i_, pvalue) in enumerate(sorted(enumerate(pvalues), lambda x, y: cmp(y[1], x[1]))):
        m.append(i_)
        if not pvalue:
            qvalues.apend(None)
        else:
            qvalues.append(min(pvalue * n / (n - c), 1))
            c += 1

    # Correct the p-values out of their proper order
    fdr = [0 for c in range(i+1)]

    for i, qvalue in enumerate(qvalues):
        if not qvalue:
            qvalues[i] = min(filter(lambda x: x != None, qvalues[:i+1]))
        if produce_ranking:
            if not qvalue:
                fp = None
            else:
                fp = int(round(qvalues[i] * (n - 1)))
            fdr[n - (i + 1)] = (m[i], qvalues[i], fp)
        else:
            fdr[m[i]] = qvalues[i]
            
    return fdr

def test(pvalues=(0.05, 0.03, 0.02, 0.01)):
    print(bonferroni_adjustment(pvalues))
    print(holm_adjustment(pvalues))
    print(fdr(pvalues))
    print(fdr(pvalues, True))
    
if __name__ == '__main__':
    test()
