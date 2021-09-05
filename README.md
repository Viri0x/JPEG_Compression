# JPEG_Compression

* Valérian FAYT <valerian.fayt>
* Romain HERMARY <romain.hermary>
* Quentin LE HELLOCO <quentin.le-helloco>
## Project
In this notebook, you have to:
* Illustrate and comment every different step of your algorithm, like if you had to explain it to someone who never heard of JPEG.
* Implement and analyses all relevant tests to demonstrate the proper functioning of the algorithm.

### Your JPEG code should at least:
* Manage color, leaving the choice to the user to compress in RGB or YUV, as well as the sub-sampling options (4:4:4, 4:2:2 and 4:2:0) of chrominance.
* Manage images whose dimensions are not 8 multiples
* Let the user choose the quality indicator q for the luminance quantification matrix.
* Return for each macro-block, a compression indicator. This indicator may be define as in the course (number of coefficient by macro-block to code without compression (64) divide by the number of coefficient not null after zigzag linearisation of the DCT quantified matrix). It can be any other relevant indicator as well, if the choice is justified.
### Bonus:
* Implement the conversion of DCT coefficients after quantification by Huffman table.
