#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_retrieve)


class Ticket:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


def reconstruct_trip(tickets, length):
    hashtable = HashTable(length)
    route = [None] * (length - 1)

    for i in tickets:
        hash_table_insert(hashtable, i.source, i.destination)
    
    route[0] = hash_table_retrieve(hashtable, "NONE")
    for i in range(1, length-1):
        val = hash_table_retrieve(hashtable, route[i-1])
        if val != None:
            route[i] = hash_table_retrieve(hashtable, route[i-1])
    
    return route
