# Angular-Differential-Imaging
Angular Differential Imaging (ADI): a technique that removes a parent star's light and reveals exoplanets.

This code requires the astropy and skimage pages Python pages.

ADI uses the rotation of the sky during an observation of a star. An average of the images take are used to subtract the parent star's light, the images are de-rotated and combined, and direct images of the exoplanets are produced.

For an excellect primer on ADI, please see Dr. Christian Thalmann's page http://web.archive.org/web/20150915005746/http://www.mpia.de/homes/thalmann/adi.htm

Steps:
1. As Earth spins on its axis, the night sky appears to rotate. 
2. Take successive pictures of a parent star. Instead of rotating the telescope to maintain the same orientation of the field of view, as one would do for a long exposure, let the field of view rotate. Record the angle between the celestial pole, the star, and zenith (the parallactic angle).
3. Median combine all of these images into an ImageMedian.
4. Subtract ImageMedian from each image to remove the parent star's light.
5. Subtract the radial profile of each image from each image to remove azimuthally symmetric sources.
6. De-rotate each image by the parallactic angle so that the exoplanets lie on top of each other when the images are combined.
7. Median combine all of the images and produce direct images of exoplanets.
