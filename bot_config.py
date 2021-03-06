# Filenames for storing seen images and twitter accounts to monitor
seen_images = "data/seen_images.txt"
twitter_accounts = "data/twitter_accounts.txt"

# identifier to start image encoding
identifier = "pr0blematic"

# temporary file for verifying the bytecode
tmp_file = "tmp_bytecode.txt"
# temporary file for the signature
tmp_sig = "tmp_sigfile.sha256"

# command file for running instructions
command_file = "command.py"

# path to the public key for rsa signatures
# created with openssl; first private key
# openssl genrsa -out [private key] 2048
# openssl rsa -in [private key] -pubout > [public key]
public_key = "tmprsa.pub"

# verify command; args: public key, signature, data to check against
verify_cmd = "openssl dgst -sha256 -verify {} -signature {} {}"
