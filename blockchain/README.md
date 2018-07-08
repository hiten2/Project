# a simple proof-of-work blockchain

# proof-of-work algorithm (pseudocode)
nonce = 0
while hash((int) data + counter) > acceptable_hash
  counter++
