#!/bin/python3

import sys

def angryProfessor(k, a):
  l = len([s for s in a if s <= 0])
  if l >= k:
    return 'NO'
  else:
    return 'YES'
    # Complete this function

if __name__ == "__main__":
    t = int(input().strip())
    for a0 in range(t):
        n, k = input().strip().split(' ')
        n, k = [int(n), int(k)]
        a = list(map(int, input().strip().split(' ')))
        result = angryProfessor(k, a)
        print(result)
