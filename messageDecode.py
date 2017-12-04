import sys
import os
import bot_config as config
import subprocess
from skimage import io              # install skimage


##########################################################
#  Decoding   
##########################################################


########################################
#
# getNbits(S,N)
#
# Functionality: get N bits from the argument string
#
# arguents:   string, number of bits to get from the beginning of the string
# return:     the N first bits of string, S
#
########################################
def getNbits(S, N):
    if not (N == 1 or N == 2 or N == 4 or N == 8 or N == 16):
        print("Density must be a member of the set, S = {1, 2, 4, 8, 16}")
        return []
    
    return S[0:N]

########################################
#
# decode(p,N)
#
# Functionality: decode pixel p at bit density N
#
# arguents:   pixel value (p) [0,255], and encode density N {1,2,4,8,16}
# return:     zero padded decoded value 
#
########################################
def decode(p, N):
    d = str(bin(p % 2**N))[2:]
    d = d.zfill(N)
    return d

def bin_to_ascii(string):
    length = len(string)
    plaintext = ""
    for i in range(0, length, 8):
        binary = string[i:i+8]
        code = int(binary, 2)
        char = chr(code)
        plaintext += char

    return plaintext

########################################
#
# getIdentifier(m,identity)
#
# Functionality: Try to find the a magic string at the start of an image, using different
#                encoding densities. 
#
# arguents:   1D image (im) and binary identifier string (identity)
# return:     Bool (good or bad message), encoding density, image with identifier removed 
#
########################################
def getIdentifier(im, identity):
    # get length of identifier string
    idLen = len(identity)

    # iterate through pixels in image, decoding at different bit densities 
    # until identifier string is found
    for N in [1,2,4,8,16]:
        for i in range(0,int(idLen / N)):
            # identifier string indicator
            match = False
            
            # check if next set of N bits match with identifier string
            if not(decode(im[i][0],N) == getNbits(identity[N*i:(N*i+N)],N)):
                match = False
                break
            else:
                match = True
                
        # if last check succeeded, the identifier was found
        if (match):
            return (True, N, im[(i+1):])
    
    # if no identifier was found, return false
    return (False,0,'')

########################################
#
# getSignature(im,encodeDensity,sigLen)
#
# Functionality: extract signature from image message 
#
# arguents:   1D image (im),encode density used to encode the message (encodeDensity),
#             and the signature length in bytes (sigLen)
# return:     signature (base 2) and image message with signature removed
#
########################################
def getSignature(im, encodeDensity, sigLen):    
    # determine how many pixels are needed to encode signature
    sigLenBin = sigLen*8
    sigLenNumPixels = int(sigLenBin / encodeDensity)
    
    # extract signature from image
    sig = ''
    for i in range(0,sigLenNumPixels):
        sig = sig + decode(im[i][0],encodeDensity)
        
    return (sig,im[sigLenNumPixels:])


########################################
#
# getPayloadLen(im,encodeDensity,pLenID)
#
# Functionality: extract payload length from image message 
#
# arguents:   1D image (im) and encode density used to encode message in image (encodeDensity),
#             and the number of bytes used to encode the payload length (pLenID)
# return:     payload length (base 10), and the message with payload length pixels removed
#
########################################
def getPayloadLen(im, encodeDensity, pLenID):
    # determine how many pixels are needed to encode payload length
    payloadLenBin = pLenID*8
    payloadLenNumPixels = int(payloadLenBin / encodeDensity)
    
    # extract payload length (base 2)
    length = ''
    for i in range(0,payloadLenNumPixels):
        length = length + decode(im[i][0],encodeDensity)

    # return payload length in bytes (base 10)
    return (int(length, 2), im[payloadLenNumPixels:])

########################################
#
# getPayload(im,encodeDensity,payloadLength)
#
# Functionality: extract payload from image message
#
# arguents:   1D image (im) and encode density used to encode message in image (encodeDensity),
#             and the payload length in bytes, base 10 (payloadLength)
# return:     binary representation of payload
#
########################################
def getPayload(im,encodeDensity,payloadLength):
    # determine how many pixels are needed to hold payload
    payloadLenBin = payloadLength*8
    payloadLenNumPixels = int(payloadLenBin / encodeDensity)
    
    payload = ''
    for i in range(0,payloadLenNumPixels):
        payload = payload + decode(im[i][0],encodeDensity)
    
    return payload

def bot(imMessage):
    # get image message dimensions
    H = imMessage.shape[0]
    W = imMessage.shape[1]
    numpixels = H*W
    
    # reshape image with message encoded in pixels
    messageIm = imMessage.reshape(numpixels*4,1)

    # indentifier key - ensure that the identifier key size >= (encodeDensity / 8) bytes 
    identifier = "pr0blematic"
    binkey = [(bin(ord(identifier[i]))[2:]).zfill(8) for i in range(0,len(identifier))]
    binIdentifier = "".join(binkey)

    # signature specifications - ensure that signature size is >= (encodeDensity / 8) bytes
    sigLen = 256 # update this with actual signature length in bytes

    # number of bytes used to represent the payload length
    pLenID = 4 # update this with actual payload identifier length in bytes

    # check for identifier, return encoding precision
    [validMessage, encodeDensity, message] = getIdentifier(messageIm, binIdentifier)
    print("Encode Density: ", encodeDensity)

    # get signature
    if (validMessage):
        print("Valid Message: Getting signature...")
        [signature, message] = getSignature(message, encodeDensity, sigLen)       
        print("WE MUST VERIFY THIS SIGNATURE")
    else:
        print("Invalid Message...")
        exit()

    # get payload length
    [payloadLength, message] = getPayloadLen(message, encodeDensity, pLenID)
    print("Payload Length: ", payloadLength, " bytes")
    
    # total number of pixels used
    numPixels = int(8 * payloadLength / encodeDensity / 4)

    # get payload
    payload = getPayload(message,encodeDensity,payloadLength)

    print("Signature: ", signature)

    ascii_sig = bin_to_ascii(signature)
    ascii_message = bin_to_ascii(payload)

    with open(config.tmp_file, "w") as f:
        f.write(payload)
    f.closed
    with open(config.tmp_sig, "w") as f:
        f.write(ascii_sig)
    f.closed

    rsa_verify_cmd = config.verify_cmd.format(config.public_key,
                        config.tmp_sig, config.tmp_file)
    verify_proc = subprocess.Popen(rsa_verify_cmd, shell=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    verification, err = verify_proc.communicate()

    if err:
        print "error verifying data: {}".format(err)
        sys.exit(1)
    if "Verified OK" not in verification:
        print "failure to verify data with public key"
        sys.exit(1)

    try:
        os.remove(config.tmp_file)
        os.remove(config.tmp_sig)
    except:
        print "error: failed to remove temporary files" 
        
    with open(config.command_file, "w") as f:
        f.write(ascii_message)
    f.closed

    proc = subprocess.Popen(["python", config.command_file], 
                    stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out, err = proc.communicate()
    if out:
        print out
    if err:
        print err

    try:
        os.remove(config.command_file)
    except:
        print "error: failed to remove command file"

    return (payload, numPixels)  




imMessage = io.imread('encodedImage.png')
[payload, numPixels] = bot(imMessage)

f = open('test.txt','w')
f.write(payload)

################################
#
# ANALYSIS
#
################################
im = io.imread('transparentImage.png')

# reshape original and encoded image into 1D array
H = im.shape[0]
W = im.shape[1]
np = H*W
im1D = im.reshape(np*4,1)
im1D_encoded = imMessage.reshape(np*4,1)

meanSquaredError = sum([((int(im1D_encoded[i][0]) - int(im1D[i][0]))**2)**(1/2) for i in range(0,np)]) / numPixels

print("\n******************************************************")
print("* Statistics:\n*")
print("*  Number of Pixels used to encode data: ", numPixels, "\n*")
print("*  Percentage of image pixels used: ", 100* numPixels / np, "% \n*")
print("*  Mean Squared Error of altered Pixels: ", meanSquaredError, "\n*")
print("******************************************************")
