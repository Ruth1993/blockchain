import string
import random
import hashlib
import time

s = 'prev_block'    #previous block in the blockchain
#x = 'reward_address' #bitcoin uses the reward address as randomization factor saving 16 bytes in coinbase. Each miner should change its reward address for privacy reasons
x = random.getrandbits(128) #random 128-bit number

#generate random attempt with s (challenge) and x (random 128-bit number to prevent miners from generating the same proof later)
def gen_attempt(challenge=s):
    found = False
    c = 0   #nonce incremented every loop to find new hash
    #xc = random.getrandbits(128) #random extra nonce

    start = time.time()
    
    while(not found):
        conc_string = hashlib.sha256((s+str(x)+str(c)).encode('ascii')).hexdigest() #compute sha256-hash of previous block, randomization factor, nonce
        if(conc_string.startswith('000000')):
            elap = time.time()-start
            found = True
            print('Hash:', conc_string)
            print('Nonce:', c)
            print('Elapsed time:', elap)
        c=c+1

    return (conc_string, elap)
