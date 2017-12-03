import byte_config as config
import subprocess
import sys
import os

# generalized function for converting ascii string to binary text
def bin_of_string(string):
    plaintext = string
    binary_text = ""

    # convert each char to ascii code, then get the binary string
    # (the most significant bit comes first)
    for char in plaintext:
        ascii_code = ord(char)
        binary = bin(ascii_code)[2:]
        bits = len(binary)
        # add padding 0s if length is less than 8
        if bits < 8:
            add = 8 - bits
            binary = ('0' * add) + binary

        # append the binary value in the order they appear in the text
        binary_text += binary

    return binary_text

def main(codefile, outfile):
    # get the binary strings of the magic strings
    binary_start = bin_of_string(config.initiator)
    binary_end = bin_of_string(config.terminator)

    # read the text from the codefile
    with open(codefile, "r") as f:
        text = f.read()
    f.closed
    
    # get the binary text for the instructions
    binary_text = bin_of_string(text)

    # write to a temporary file for signing
    with open(config.tmp_file, "w") as f2:
        f2.write(binary_text)
    f2.closed

    # use the cmd from the config to sign the instruction binary to stdout
    rsa_sign_cmd = config.sign_cmd.format(config.private_key, config.tmp_file)
    sign_proc = subprocess.Popen(rsa_sign_cmd, shell=True, 
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    signature, err = sign_proc.communicate()
    
    # alert the user and exit if there is an error
    if err:
        print "error signing data: {}".format(err)
        sys.exit(1)

    # try to remove the temporary file and alert if there is an error
    try:
        os.remove(config.tmp_file)
    except:
        print "error removing {}".format(config.tmp_file)

    # binary text of the sha256 hash signature
    binary_signature = bin_of_string(signature)

    # final binary: [initiator][signature][instructions][terminator]
    final_binary = binary_start + binary_signature + binary_text + binary_end

    if outfile:
        with open(outfile, "w") as f3:
            f3.write(final_binary)
        f3.closed 
    else:
        print final_binary

if __name__ == "__main__":
    args = sys.argv
    try:
        codefile = args[1]
    except:
        print "usage: python binary_convert.py [file]"
        sys.exit(1)

    try:
        outfile = args[2]
    except:
        outfile = ""

    main(codefile, outfile)
