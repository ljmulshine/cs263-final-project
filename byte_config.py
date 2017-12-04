# magic strings for starting command instructions
initiator = "pr0blematic"

# path to the private key for rsa signatures
# created with the command 'ssh -t rsa'
private_key = "/home/jsteeves/.ssh/tmp_rsa"

# temporary file for signing the bytecode
tmp_file = "tmp_bytecode.txt"

# the command for signing the bytecode
sign_cmd = "openssl dgst -sha256 -sign {} -out /dev/stdout {}"
