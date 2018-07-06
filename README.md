# LSSTprep
Repository for Richards group LSST prep work, specifically related to the AGN SC.  Maintained by gtr@physics.drexel.edu
 
LCmerge -- Notebooks related to trying to understand how we can best
merge light curves from multiple bands to produce a single light
curve, both for the purpose of deciding whether an object is variable
or not and for determining the properties of the variability.  Started
by Drexel undergrad Jared Haughton (Drexel 2018), currently maintained
by Drexel undergrad co-op student Rachel Buttry (Drexel 2019).

GAIA -- Notebooks related to determining under what conditions GAIA can be used to improve quasar selection in LSST.  The bottom line is roughly that all quasars brighter than $i=20$ will be detected by GAIA, but essentially no quasars fainter than $i=22$ will be.  Currently maintained by Drexel undergrad co-op student Bee Martin (Drexel 2020).

Photoz -- Notebooks exploring different aspect of photo-z's for AGNs
in LSST.  Currently maintained by Drexel undergrad co-op student Bee
Martin (Drexel 2020).  The point is to demonstrate that photo-z in the LSST era will need to consider AGNs with significant contributions from their host galaxy where photo-z algorithms for quasars are more prone to fail (due to host contamination) and where photo-z algorithms for galaxies are also more prone to fail (due to central engine contamination).  We compare the effectiveness of 4 galaxy photo-z algorithms used by DES with our own Nadaraya-Watson based quasar photo-z algorithm.  <br>
<ul>
<li> https://github.com/RichardsGroup/LSSTprep/blob/master/Photo-z/DESvNWcomparison_sdss_quasars.ipynb contains comparisons of DES methods and our NW method for SDSS DR7 and DR12 quasars matched to DES sva1.  </li>
<li> https://github.com/RichardsGroup/LSSTprep/blob/master/Photo-z/DESvsNWcomp_gtr_stars.ipynb contains similar comparisons for "stars" from GTR-ADM-QSO-ir-testhighz_findbw_lup_2016_starclean.fits (https://github.com/gtrichards/QuasarSelection/blob/master/data/GTR-ADM-QSO-ir-testhighz_findbw_lup_2016_starclean.fits), hereafter GTR, matched to DES sva1. </li>
</ul>
There are two other notebooks, containing similar comparisons for quasars from GTR and a combined dataset of SDSS quasars and GTR objects matched to DES, however these are not the focus and are not being maintained actively.  
In general, our comparisons show that the 4 DES methods perform well for low redshift extended sources, but greatly underestimate point sources when compared to our Nadaraya-Watson method, which also handles low redshift objects and is correct on average with high spread at higher redshifts. 



