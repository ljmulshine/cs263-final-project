import byte_config as config
import subprocess
import sys
import os


def byte_of_string(string):
    plaintext = string
    binary_text = ""
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

        # a print statement for testing values
        #print char, ascii_code, bin(ascii_code), binary
    return binary_text

def main(codefile):
    # read the text from the codefile
    with open(codefile, "r") as f:
        text = f.read()
    f.closed
    
    # convert each char to ascii code, then get the binary string
    # (the most significant bit comes first)
    binary_start = byte_of_string(config.initiator)
    binary_end = byte_of_string(config.terminator)
    binary_text = byte_of_string(text)

    with open(config.tmp_file, "w") as f2:
        f2.write(binary_text)
    f2.closed

    rsa_sign_cmd = config.sign_cmd.format(config.private_key, config.tmp_file)
    sign_proc = subprocess.Popen(rsa_sign_cmd, shell=True, 
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    signature, err = sign_proc.communicate()
    if err:
        print "error signing data: {}".format(err)
        sys.exit(1)

    try:
        os.remove(config.tmp_file)
    except:
        print "error removing {}".format(config.tmp_file)

    binary_signature = byte_of_string(signature)

    final_binary = binary_start + binary_signature + binary_text + binary_end

    print final_binary

if __name__ == "__main__":
    args = sys.argv
    try:
        codefile = args[1]
    except:
        print "usage: python binary_convert.py [file]"
        sys.exit(1)

    main(codefile)
