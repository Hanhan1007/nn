import math
import h5py
import argparse
from dset import BrownCorpus
from os.path import join as pjoin

'''
Compute perplexity given a set of likelihoods and labels
'''

def compute_pp(likelihoods, labels):
    # Working in log space
    pp = 0.0

    N = likelihoods.shape[1]
    assert N == labels.size
    for k in xrange(N):
        pp = pp - math.log(likelihoods[labels[k], k])
    pp = pp / N

    pp = math.exp(pp)

    return pp

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('likelihoods_file', help='File containing likelihoods')
    args = parser.parse_args()

    # FIXME PARAM
    context_size = 4
    batch_size = 512
    dataset = BrownCorpus(context_size, batch_size, subset='dev')
    labels = dataset.labels

    h5f = h5py.File(args.likelihoods_file)
    likelihoods = h5f['likelihoods'][...]

    pp = compute_pp(likelihoods, labels)

    print 'Perplexity: %f' % pp
    print 'Bits/unit: %f' % math.log(pp, 2)