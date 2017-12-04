import sys
from skimage import io              # install skimage
import matplotlib.pyplot as plt     # install matplotlib

# bytecode is encoded in image starting at upper left pixel 
# and moving 1st in the x direction and then in the y direction
#        -->-->-->
#  (1)   o o o o o o o o 
#  (2)   o o o o o o o o
#  (3)   o o o o o o o o
#  (4)   o o o o o o o o

########################################
#
# getNbits(f,N)
#
# Functionality: split contents of .txt file, f, into N bit chunks
#
# arguents:   .txt file, number of bits used to segment .txt file
# return:     array containing N-bit chunks of .txt file, f
#
########################################
def split2Nbits(f, N):
    if not (N == 1 or N == 2 or N == 4 or N == 8 or N == 16):
        print("Density must be a member of the set, S = {1, 2, 4, 8, 16}")
        return []
    
    data = f.read()
    return [data[i:i+N] for i in range(0,len(data),N)]

########################################
#
# b2d(s)
#
# Functionality: convert binary string to its corresponding decimal value
#
# arguents:   binary number as a string (s)
# return:     decimal representation of binary input string
#
########################################
def b2d(s):
    srev = s[::-1]
    val = 0
    i = 0
    for b in srev:
        val = val + int(b) * 2**i
        i = i + 1
    return val

########################################
#
# encodeData(im1D, encodeDensity, payload)
#
# Functionality: encode payload data in image with specified encode density,
#                where encode density refers to the number of bits encoded 
#                in each pixel
#
# arguents:   1-D image array (im1D), encode density (encodeDensity), payload data (payload)
# return:     1-D image array containing encoded data
#
########################################
def encodeData(im1D, encodeDensity, payload):
    for i in range(0,len(payload)):
        value = b2d(payload[i])

        # current pixel
        p = im1D[i][0]

        # pixel with encoded info
        pnew = (p - (p % 2**encodeDensity) + value)
        
        # verify that new pixel value is in range [0, 255]
        if (pnew > 255):
            im1D[i][0] = (p - (p % 2**encodeDensity) - (2**encodeDensity - value))
        else:
            im1D[i][0] = pnew
    
        # verify that pixel value was correctly encoded
        if not (pnew % 2**encodeDensity == value):
            print(value)
            print("error!!", p, " ",pnew)
            break
    
    return im1D

            
def CandC(imFile, bytecodeFile, encodeDensity):
    # read in image of dog
    im = io.imread(imFile)

    # show dog image
    plt.figure()
    plt.imshow(im)
    plt.show()

    # get image dimensions
    H = im.shape[0]
    W = im.shape[1]
    numpixels = H*W

    # reshape image into N x 1 array, where N = numPixels * 3
    im1D = im.reshape(numpixels*3,1)

    # open binary code file
    f = open(bytecodeFile, 'r')

    # split binary code file into N-bit chunks, where N = encodeDensity
    data = split2Nbits(f,encodeDensity)
    im1D = encodeData(im1D, encodeDensity, data)

    # reshape image with encoded data into regular image form
    imMessage = im1D.reshape(H,W,3)

    plt.figure()
    plt.imshow(imMessage)
    plt.show()
    f.close()
    
    io.imsave('encodedImage.png', imMessage)
    return imMessage


# encode density
encodeDensity = 2

# image file
imFile = 'dog.png'

# bytecode file
bytecodeFile = 'binary_code.txt'

# generate image with encoded data
imMessage = CandC(imFile, bytecodeFile, encodeDensity)