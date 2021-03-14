import collections, functools, itertools, heapq, statistics, bisect, math, sys, sortedcontainers, random, time, datetime, csv, re, multiprocessing
from collections import deque, Counter, defaultdict, OrderedDict
from functools import lru_cache
from itertools import permutations, accumulate
from heapq import (
    heappush,
    heappop,
    heapreplace,
    heappushpop,
    heapify,
    merge,
    nlargest,
    nsmallest,
    _heappop_max,
    _heapify_max,
    _heapreplace_max,
    _siftdown_max,
)
from statistics import mean, median, mode
from bisect import bisect_right, bisect_left
from math import (
    floor,
    ceil,
    log2,
    log,
    log10,
    sqrt,
    factorial,
    gamma,
    lgamma,
    pi,
    e,
    inf,
)
from sys import maxsize, stdin
from sortedcontainers import SortedList, SortedDict, SortedSet
from random import seed, randrange, randint, random, choice, choices
from time import localtime, strftime, mktime
from datetime import datetime
from csv import reader, writer
from re import search
from multiprocessing import Pool
import json

class UnionFind:
    def __init__(self, N):
        self.p = [i for i in range(N)]

    def find(self, u):
        if self.p[u] == u:
            return u
        self.p[u] = self.find(self.p[u])
        return self.p[u]

    def same(self, u, v):
        return self.find(u) == self.find(v)

    def join(self, u, v):
        u = self.find(u)
        v = self.find(v)
        if u == v:
            return
        self.p[u] = v

matchings = ['Email', 'Phone', 'OrderId']
VERSION = 3

def solve():
    dataset = None
    with open('contacts.json') as f:
        dataset = json.loads(f.read())

    with open('formatted.txt', 'w') as f:
        for d in dataset:
            f.write(f"{d}\n")

    N = len(dataset)
    print(f"dataset len: {N}")

    uf = UnionFind(N)
    M = len(matchings)
    first = [{} for i in range(M)]

    for idx in range(N):
        entry = dataset[idx]
        vals = [entry[col] for col in matchings]
        for i in range(M):
            if vals[i] == '':
                continue
            if vals[i] not in first[i]:
                first[i][vals[i]] = idx
            else:
                uf.join(first[i][vals[i]], idx)

    owned = defaultdict(list)
    total = defaultdict(int)
    maxTotal = 0
    for i in range(N):
        p = uf.find(i)
        owned[p].append(str(i))
        total[p] += dataset[i]['Contacts']
        maxTotal = max(maxTotal, total[p])

    print("stage e")
    print(f"maxTotal: {maxTotal}")

    ans = {}
    for p in set(uf.p):
        ans[p] = f"{'-'.join(owned[p])}, {total[p]}"

    print("stage f")

    with open(f'{VERSION}.csv', 'w') as f:
        f.write('ticket_id,ticket_trace/contact\n')
        for i in range(N):
            p = uf.find(i)
            f.write(f'{i},"{ans[p]}"\n')
            
def verify():
    dataset = None
    with open('contacts.json') as f:
        dataset = json.loads(f.read())

    for idx, entry in enumerate(dataset):
        assert(idx == entry['Id'])

    skipped = False
    verifset = []
    with open(f'{VERSION}.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if not skipped:
                skipped = True
                continue
            cols = row[1].split(',')
            verifset.append([list(map(int, cols[0].split('-'))), int(cols[1].strip())])

    for tids, total in verifset:
        cnt = 0
        for tid in tids:
            cnt += dataset[tid]['Contacts']
        assert(cnt == total)
        
        uf = UnionFind(len(tids))
        for i in range(len(tids)):
            for j in range(i):
                for matching in matchings:
                    if dataset[tids[i]][matching] == '' or dataset[tids[j]][matching] == '':
                        continue
                    uf.join(i, j)
                    break
        for i in range(len(tids)):
            uf.find(i)
        assert(len(set(uf.p)) == 1)
    
if __name__ == "__main__":
    solve()
    verify()

