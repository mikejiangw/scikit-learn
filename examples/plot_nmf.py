"""
===================================================
NMF for digits feature extraction
===================================================

NMF with sparseness enforced in the components,
in comparison with RandomizedPCA for feature
extraction.


"""


print __doc__

from time import time
import logging
import numpy as np
import pylab as pl

from scikits.learn.pca import RandomizedPCA
from scikits.learn.nmf import NMF
from scikits.learn import datasets


# Display progress logs on stdout
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
                    
digits = datasets.load_digits()

# reshape the data using the traditional (n_samples, n_features) shape
n_samples = len(digits.images)
X = digits.images.reshape((n_samples, -1))
n_features = X.shape[1]

################################################################################
# Compute a PCA (eigenfaces) on the face dataset (treated as unlabeled
# dataset): unsupervised feature extraction / dimensionality reduction
n_components = 16

print "Extracting the top %d eigendigits from %d images" % (
    n_components, X.shape[0])
t0 = time()
pca = RandomizedPCA(n_components=n_components, whiten=True).fit(X)
print "done in %0.3fs" % (time() - t0)

eigendigits = pca.components_.T

#print "Projecting the data on the eigenfaces orthonormal basis"
#t0 = time()
#X_pca = pca.transform(X)
#print "done in %0.3fs" % (time() - t0)

################################################################################
# Compute the NMF on the same data
print "Extracting %d non-negative features from %d images" % (
    n_components, X.shape[0])
t0 = time()
nmf = NMF(n_components=n_components, init='nndsvd', beta=5, tol=1e-2,
          sparseness="components").fit(X)
print "done in %0.3fs" % (time() - t0)

nmfdigits = nmf.components_.T

################################################################################
# Plotting the results

n_row, n_col = 4, 4

f1 = pl.figure(figsize=(1.8 * n_col, 2.4 * n_row))
f1.text(.5, .95, 'Principal components', horizontalalignment='center') 
pl.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.35)
for i in range(n_row * n_col):
    pl.subplot(n_row, n_col, i + 1)
    pl.imshow(eigendigits[i].reshape((8, 8)), cmap=pl.cm.gray)
    pl.xticks(())
    pl.yticks(())

f2 = pl.figure(figsize=(1.8 * n_col, 2.4 * n_row))
f2.text(.5, .95, 'Non-negative components', horizontalalignment='center') 
pl.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.35)
for i in range(n_row * n_col):
    pl.subplot(n_row, n_col, i + 1)
    pl.imshow(nmfdigits[i].reshape((8, 8)), cmap=pl.cm.gray)
    pl.xticks(())
    pl.yticks(())  

pl.show()