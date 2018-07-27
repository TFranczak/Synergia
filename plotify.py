import matplotlib.pyplot as plt
import h5py
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: plotify.py <h5 file> <h5 file>"
        Exit()


    # Open first file
    h5_1 = h5py.File(sys.argv[1])
    h5_2 = h5py.File(sys.argv[2])
