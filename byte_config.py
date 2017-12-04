# magic strings for starting command instructions
initiator = "pr0blematic"

# path to the private key for rsa signatures
# created with openssl; first private key
# openssl genrsa -out [private key] 2048
# openssl rsa -in [private key] -pubout > [public key]
private_key = "tmprsa.key"
public_key = "tmprsa.pub"

# temporary file for signing the bytecode
tmp_file = "tmp_bytecode.txt"

# the command for signing the bytecode; args: private key, data file
sign_cmd = "openssl dgst -sha256 -sign {} -out /dev/stdout {}"

# verify command; args: public key, signature, data to check against
verify_cmd = "openssl dgst -sha256 -verify {} -signature {} {}"
