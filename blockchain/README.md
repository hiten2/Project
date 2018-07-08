# a simple proof-of-work blockchain

# proof-of-work algorithm (pseudocode)
nonce = 0
while hash((int) data + nonce) > acceptable_hash
  nonce++
