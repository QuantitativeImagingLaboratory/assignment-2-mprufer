Discrete Fourier Transform
--------------------------
I use 4 different for loops to calculate the fourier transform for each
index. The first two for loops is to make sure the final summation
calculated is indexed correctly for the output matrix. The inner two for
loops is to iterate through the input matrix to calculate the summation
which, at the end of the two inner for loops, is the fourier transform
for that index and is indexed in the output matrix at the end of both
those loops.
The values calculated at the end are very large. At first, I had written
code to only get the last 3 digits after the decimal and index that.
However, when the matrix is passed on to the other functions it was
slightly off so I kept the entire summation instead.

Inverse Fourier Transform
-------------------------
My method for the inverse is the same as the forward transform, except
the sine value is added rather than subtracted. The overall structure of
the algorithm is the same, however.
For this, I got frustrated because I kept assuming you were supposed to
get the original input matrix's values back, which is generally how it
does work. After getting feedback however, I learned that you do get
complex values back and the it won't necessarily be the original input
matrix's values I would get back either. Rather, to make sure it's
correct, I should make sure the shift between numbers is consistent.

Magnitude
---------
For this, I just took the absolute value of the input matrix since the
numpy library's absolute function will return the magnitude of complex
numbers.
The results showed that the magnitude is pretty much the same as the
real number component of the inverse fourier transform, albeit with some
small plus/minus value that is represented by the imaginary component.

Discrete Cosine Transform
-------------------------
For this, I just took the algorithm from my fourier transform and deleted
the portion that calculated for the sine value. Other than that, the
algorithm remains the same.

Ideal Pass Filtering
--------------------
The algorithm for this is very straightforward. I just get the shape of
the image, make an empty matrix to hold the filter values, then calculate
the distance and index that value in the previously created empty matrix.
The high pass filtering calls upon low-pass then I do: 1-lowpass value
to get the high pass mask value since the high pass is just an inverse
of the low pass mask.
Once I pass the mask, I multiply it to the fourier transform of the image,
do a full contrast stretch, then pass the image back.
For ideal, I noticed higher cutoff values did not blur the image much
while much lower values blurred it much more. Also, the resulting image
had "ringing" around the edges so the resulting image is not very clean.
This is apparent in the high pass filter as well, with the edges not
being as straight or clean.

Butterworth Filtering
---------------------
For butterworth, I had to use the same algorithm twice in both low and
high pass, withe difference in high pass being I divide by the distance
rather than then cutoff value like in low pass.
The resulting image for the butterworth low pass filter creates a much
more smooth blurring effect with no ringing. The high pass filter resulted
in an image similar to ideal high pass but with less noise.

Gaussian Filtering
------------------
The Gaussian filtering is similar to the ideal high pass (except in the
formula used to calculate the mask). In the Gaussian high pass, I called
on the Gaussian low pass, then I did: 1-lowmask for each index in the mask.
The resulting images were a much smoother blurring for the low pass (but
it had less of a blurring effect than butterworth filtering) and a high
pass image similar to the butterworth filtering but with more noise.

Filtering
---------
I used the numpy library to calculate the fourier transform to just get
one resulting matrix. Then I shifted the image. When passing back the
fourier transform as an image, I did a logarithmic compression of the
magnitude but found all I got was a completely black image back. So I
passed the image to post_process_image to do a full-contrast stretch and
get a visible image back of the fourier transform.
To make sure the correct number of arguments are passed to the filter functions,
I searched the filter argument passed for the filters then passed the
corresponding arguments.
After that, I applied the mask by multiplying it to the shifted fourier
transform. For the filtered DFT image, I only needed to pass back the image
after multiplying the fourier transform to the mask since the fourier
transform's magnitude has been already logarithmically compressed and passed
through post_process_image.
After that, another shit and the inverse fourier transform is applied.
For the high pass filtered image to be better visible, I took the negative
of the resulting image. The reason for not performing this in post_process_image
was to make sure that the DFT and filtered DFT were not taken negatives of.
I only wanted the filtered image from high pass filtering to be taken the
negative of.

Post-Process Image
------------------
To perform the full-contrast stretch, I first iterated through the image
to find the max and min pixel intensities in the image. After that, I applied
the for formula for full-contrast stretch and indexed the new value in
image matrix. Then it is converted to gray-scale and passed back.