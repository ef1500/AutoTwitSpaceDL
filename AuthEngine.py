# AuthEngine
# Written by ef1500
# Written so that we can bypass the use of proxies, and still monitor an absurd amount of users.
import functools as kaede
import random

# Create a functions that allows us to load up all of the user tokens and store them in a list that's cached so we can
# call it efficently later on
@kaede.lru_cache
def LoadTokens(file):
    with open(file, 'r') as TokenLoader:
        tokens = [line.strip() for line in TokenLoader]
    TokenLoader.close()
    return tokens
    
# Let's now make another function that will let us spread the amount of monitored users across multiple accounts
def GetToken(tokens):
    if len(tokens) <= 1:
        return tokens[0]
    else:
        return tokens[random.randrange(len(tokens))] # Return a random token