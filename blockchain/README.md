# a simple proof-of-capacity blockchain

# proof-of-capacity algorithm (pseudocode)
nonce = 0
while hash((int) data + nonce) > acceptable_hash
  nonce++
