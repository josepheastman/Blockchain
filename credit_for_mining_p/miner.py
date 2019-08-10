import hashlib
import requests

import sys


# TODO: Implement functionality to search for a proof 
def proof_of_work(last_block_string):
    """
    Simple Proof of Work Algorithm
    Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes
    """
    print("Starting work on a new proof")
    proof = 0

    # for block 1, hash(1, p) = 000000x
    while not valid_proof(last_block_string, proof):
        proof += 1
    print("Sending request to server")
    return proof

def valid_proof(last_block_string, proof):
    guess = f'{last_block_string}{proof}'.encode()
    # ise hash function
    guess_hash = hashlib.sha256(guess).hexdigest()
    # check if 6 leading 0's in hash result
    beg = guess_hash[0:6]  # [:6]
    if beg == "000000":
         return True
    else:
        return False

if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:

        # generate request with /last_block_string

        r = requests.get(url = node + '/last_block_string')
        data = r.json()
        last_block_string = data['last_block_string'] ['previous_hash']
        
        # look for a new one
        print(last_block_string)
        new_proof = proof_of_work(last_block_string)
        
        #  When found, POST it to the server {"proof": new_proof}
        # {"proof": new_proof}


        # We're going to have to research how to do a POST in Python
        # HINT: Research `requests` and remember we're sending our data as JSON
        proof_data = {
            'proof': new_proof
        }


        r = requests.post(url = node +'/mine', json = proof_data)
        data = r.json()

        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined (for this client) and print it.  Otherwise,
        # print the message from the server.
        if data.get('message') == "New Block Forged":
            coins_mined +=1
            print("You have: " + str(coins_mined) + " coins")
        print(data.get('message'))
