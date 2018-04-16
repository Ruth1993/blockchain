import string
import random
import hashlib
import time
from datetime import datetime

s = 'prev_block'    #previous block in the blockchain
#x = 'reward_address' #bitcoin uses the reward address as randomization factor saving 16 bytes in coinbase. Each miner should change its reward address for privacy reasons

#generate random attempt with s (challenge) and x (random 128-bit number to prevent miners from generating the same proof later)
def gen_attempt(z):
    found = False
    c = 0   #nonce incremented every loop to find new hash
    x = random.getrandbits(128) #random 128-bit number

    start = time.time()
    
    while(not found):
        conc_string = hashlib.sha256((s+str(x)+str(c)).encode('ascii')).hexdigest() #compute sha256-hash of previous block, randomization factor, nonce
        
        if(conc_string.startswith("".join(["0"]*z))):
            elap = time.time()-start
            found = True
            print('Hash:', conc_string)
            print('Nonce:', c)
            print('Elapsed time:', elap)
            print()
        c=c+1

    return conc_string
