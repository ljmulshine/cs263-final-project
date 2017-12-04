# magic strings for starting command instructions
initiator = "pr0blematic"

# path to the private key for rsa signatures
# created with openssl; first private key
# openssl genrsa -out [private key] 2048
# openssl rsa -in [private key] -pubout > [public key]
private_key = "tmprsa.key"

# temporary file for signing the bytecode
tmp_file = "tmp_bytecode.txt"

# the command for signing the bytecode; args: private key, data file
sign_cmd = "openssl dgst -sha256 -sign {} -out /dev/stdout {}"
