import netsquid
import numpy as np
from application import AliceProgram, BobProgram
from matplotlib import pyplot

from squidasm.run.stack.config import (
    GenericQDeviceConfig,
    StackConfig,
    StackNetworkConfig,
)
from squidasm.run.stack.run import run

# We use the density matrix formalism for the qubits.
# This allows one to absorb the effects of depolarization into the density matrix and improve the fidelity calculation.
netsquid.set_qstate_formalism(netsquid.QFormalism.DM)


# import network configuration from file
cfg = StackNetworkConfig.from_file("config.yaml")

# Create instances of programs to run, specify the angles for the state of the teleportation qubit
alice_program = AliceProgram(theta=0.0, phi=0.0)
bob_program = BobProgram()

# Run the simulation. Programs argument is a mapping of network node labels to programs to run on that node
run(config=cfg, programs={"Alice": alice_program, "Bob": bob_program}, num_times=1)
