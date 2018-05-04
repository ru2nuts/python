class Node(object):

    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next = next_node


"""
 Print elements of a linked list in reverse order as standard output
 head could be None as well for empty list
 Node is defined as

 class Node(object):

   def __init__(self, data=None, next_node=None):
       self.data = data
       self.next = next_node


"""


def has_cycle(head):
    fp = head
    sp = head

    while fp != None and sp != None:
        if (fp.next == None):
            return False
        sp = sp.next
        fp = fp.next.next
        if fp == sp:
            return True
    return False



n0 = Node(data=0, next_node=None)
n1 = Node(data=1, next_node=n0)
n2 = Node(data=2, next_node=n1)
n3 = Node(data=3, next_node=n2)
n4 = Node(data=4, next_node=n3)
n5 = Node(data=5, next_node=n4)
n6 = Node(data=6, next_node=n5)

print (has_cycle(n6))

n0.next=n0

print (has_cycle(n6))



def ReversePrint(head):
    if (head == None):
        return
    c = head
    rr = Node(data=c.data, next_node=None)
    while c != None:
        if (c.next != None):
            rr = Node(data=c.next.data, next_node=rr)
        c = c.next

    rc = rr
    while (rc != None):
        print(rc.data)
        rc = rc.next

