import matplotlib.pyplot as plt
import h5py
import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise ValueError('Usage: plotify.py <h5 file> <h5 file>')

    # Open hdf5 files
    h5_1 = h5py.File(sys.argv[1])
    h5_2 = h5py.File(sys.argv[2])

    # Finds elens amplitude from output file names
    amp1 = sys.argv[1].split('_')[1]
    amp2 = sys.argv[2].split('_')[1]


    # Plot x emittance from both -----------------------------------
    plt.xlabel("Distance (m)")
    plt.ylabel("Emittance (m)")
    plt.title("X Emittance for " + amp1 + " and " + amp2 + " VS Distance")

    plt.plot(h5_1.get("s"), h5_1.get("emitx"), label='X Emit for ' + sys.argv[1].split('_')[1])
    plt.plot(h5_2.get("s"), h5_2.get("emitx"), label='X Emit for ' + sys.argv[2].split('_')[1])
    plt.tight_layout()
    plt.legend()
    plt.show()

    # Plot y emittance from both ------------------------------------
    plt.xlabel("Distance (m)")
    plt.ylabel("Emittance (m)")
    plt.title("Y Emittance for " + amp1 + " and " + amp2 + " VS Distance")

    plt.plot(h5_1.get("s"), h5_1.get("emity"), label='Y Emit for ' + sys.argv[1].split('_')[1])
    plt.plot(h5_2.get("s"), h5_2.get("emity"), label='Y Emit for ' + sys.argv[2].split('_')[1])
    plt.tight_layout()
    plt.legend()
    plt.show()

