import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random


def proof_of_work(last_proof, attempts=1000000):

    start = timer()
    random.seed()

    print("Searching for next proof")
    lFive = lastFive(last_proof)
    proof = random.randint(-8000000000000000000, 8000000000000000000)
    for i in range(attempts):
        proofString = str(proof + i)
        if valid_proof(lFive, proofString):
            print("We got a proof: " + proofString + " took us " + str(timer() - start))
            return proofString

    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof

    print("Could not find proof in " + str(timer() - start))
    return None

def lastFive(last_proof):
    encodedProof = str(last_proof).encode()
    last_hash = hashlib.sha256(encodedProof).hexdigest()
    return last_hash[-5:]


def valid_proof(last_hash, proof):
    guess = proof.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:5] == lastFive


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    f = open(r"C:\Users\Justin\Documents\GitHub\Sprint-Challenge--Hash-BC\blockchain\my_id.txt")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
