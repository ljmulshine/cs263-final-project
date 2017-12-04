import sys

def main(codefile):
    # read the text from the codefile
    with open(codefile, "r") as f:
        text = f.read()
    f.closed
    
    # convert each char to ascii code, then get the binary string
    # (the most significant bit comes first)
    binary_text = ""
    for char in text:
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

    print binary_text

if __name__ == "__main__":
    args = sys.argv
    try:
        codefile = args[1]
    except:
        print "usage: python binary_convert.py [file]"
        sys.exit(1)

    main(codefile)
