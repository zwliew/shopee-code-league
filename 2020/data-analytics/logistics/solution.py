import collections, functools, itertools, heapq, statistics, bisect, math, sys, sortedcontainers, random, time, datetime, csv
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
import re


def main():
    SLA = {}
    SLA["metro manila"] = {}
    SLA["luzon"] = {}
    SLA["visayas"] = {}
    SLA["mindanao"] = {}
    SLA["metro manila"]["metro manila"] = 3
    SLA["metro manila"]["luzon"] = 5
    SLA["metro manila"]["visayas"] = 7
    SLA["metro manila"]["mindanao"] = 7
    SLA["luzon"]["metro manila"] = 5
    SLA["luzon"]["luzon"] = 5
    SLA["luzon"]["visayas"] = 7
    SLA["luzon"]["mindanao"] = 7
    SLA["visayas"]["metro manila"] = 7
    SLA["visayas"]["luzon"] = 7
    SLA["visayas"]["visayas"] = 7
    SLA["visayas"]["mindanao"] = 7
    SLA["mindanao"]["metro manila"] = 7
    SLA["mindanao"]["luzon"] = 7
    SLA["mindanao"]["visayas"] = 7
    SLA["mindanao"]["mindanao"] = 7

    with open("submission.csv", "w") as out_file:
        out_file.write("orderid,is_late\n")
        with open("delivery_orders_march.csv", encoding="utf-8") as in_file:
            in_reader = reader(in_file)
            read_header = False

            for row in in_reader:
                if not read_header:
                    read_header = True
                    continue

                order_id, pick, first, second, origin, dest = row

                origin = find_location(origin.lower())
                dest = find_location(dest.lower())

                pick = int(pick)
                first = int(float(first))
                pick = localtime(pick)
                first = localtime(first)
                if first < pick:
                    print(pick, first)
                if second != "":
                    second = int(float(second))
                    second = localtime(second)
                else:
                    second = None

                pick = pick.tm_mday + (31 if pick.tm_mon == 4 else 0)
                first = first.tm_mday + (31 if first.tm_mon == 4 else 0)
                if second:
                    second = second.tm_mday + (31 if second.tm_mon == 4 else 0)

                if count_working_days(pick, first) > SLA[origin][dest]:
                    out_file.write(f"{order_id},1\n")
                    continue

                if second:
                    if count_working_days(first, second) > 3:
                        out_file.write(f"{order_id},1\n")
                        continue

                out_file.write(f"{order_id},0\n")


def find_location(location_str):
    locations = ["metro manila", "luzon", "visayas", "mindanao"]
    for location in locations:
        if re.search(r'\b' + location + r'\b', location_str):
            return location
    return None


def count_working_days(start, end):
    holidays = {1, 8, 15, 22, 25, 29, 30, 31, 36, 43, 50, 57}
    total = end - start
    for holiday in holidays:
        if holiday >= start and holiday <= end:
            total -= 1
    return total


main()
