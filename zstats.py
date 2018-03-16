#!/usr/bin/env python
import sys, os
import re

CORENAME = "xeoncore"
cycPattern = "\s" + CORENAME + "-[0-9]+"
l2Pattern = "\sl2-[0-9]+"
l3Pattern = "\sl3-[0-9]+"
memPattern = "\smem-[0-9]+"

if __name__ == '__main__':
    filepath = None
    if os.path.isfile('./zsim.out'):
        filepath = './zsim.out'
    if len(sys.argv) > 1:
         if os.path.isfile(sys.argv[1]):
              filepath = sys.argv[1]
         if os.path.isfile(sys.argv[1] + '/zsim.out'):
            filepath = sys.argv[1] + '/zsim.out'

    if not filepath:
        print("usage: %s <zsim.out>" % sys.argv[0])
        sys.exit(0)

    cycleSum = instrSum = 0
    l2Hits = l2Misses = 0
    l3Hits = l3Misses = 0
    mReads = mWrites = 0
    mReadsDueToWriteMiss = 0

    with open(filepath, "r") as f:
        lines = f.readlines()

        for i, line in enumerate(lines):
            if re.search(cycPattern, line):
                cycles = int(lines[i+1].split()[1])
                cycleSum += cycles

                instrs = int(lines[i+3].split()[1])
                instrSum += instrs

            if re.search(l2Pattern, line):
                hGETS = int(lines[i+1].split()[1])
                hGETX = int(lines[i+2].split()[1])
                l2Hits += (hGETS + hGETX)

                mGETS = int(lines[i+3].split()[1])
                mGETXIM = int(lines[i+4].split()[1])
                mGETXSM = int(lines[i+5].split()[1])
                l2Misses += (mGETS + mGETXIM + mGETXSM)

            if re.search(l3Pattern, line):
                hGETS = int(lines[i+1].split()[1])
                hGETX = int(lines[i+2].split()[1])
                l3Hits += (hGETS + hGETX)

                mGETS = int(lines[i+3].split()[1])
                mGETXIM = int(lines[i+4].split()[1])
                mGETXSM = int(lines[i+5].split()[1])
                l3Misses += (mGETS + mGETXIM + mGETXSM)
                mReadsDueToWriteMiss += mGETXIM

            if re.search(memPattern, line):
                mReads += int(lines[i+1].split()[1])
                mWrites += int(lines[i+2].split()[1])


    print("-" * 60)

    print("Total sim cycles: " + "{:,}".format(cycleSum))
    print("Total sim unhalted instructions: " + "{:,}".format(instrSum))
    print("Total sim IPC: " + str(float(instrSum) / cycleSum))

    print("Total L2 Hits:\t\t" + "{:,}".format(l2Hits))
    print("Total L2 Misses:\t" + "{:,}".format(l2Misses))

    print("Total L3 Hits:\t\t" + "{:,}".format(l3Hits))
    print("Total L3 Misses:\t" + "{:,}".format(l3Misses))

    print("Write-miss reads:\t" + "{:,}".format(mReadsDueToWriteMiss))
    print("Total Mem Reads:\t" + "{:,}".format(mReads))
    print("Total Mem Writes:\t" + "{:,}".format(mWrites))
    print("-" * 60)
    print("Effective Mem Reads:\t" + "{:,}".format(mReads - mReadsDueToWriteMiss))
    print("Effective Mem Writes:\t" + "{:,}".format(mWrites))

    print("-" * 60)

    print("L2 MPKI: " + str(float(l2Misses) / (instrSum / 1000)))
    print("L3 MPKI: " + str(float(l3Misses) / (instrSum / 1000)))
