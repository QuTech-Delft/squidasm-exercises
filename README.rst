Exercises spring school 2024
+++++++++++++++++++++++++++++++++++++++++

introduction
--------------
This folder contains the starting point for exercises in learning SquidASM.
To do these exercises SquidASM (version 0.12.1) must be installed.
The installation instructions for SquidASM can be found on:
`SquidASM installation <https://squidasm.readthedocs.io/en/latest/installation.html>`_

The aim of these exercises is to make the user write their own teleportation routine
and investigate the fidelity of the teleported qubit vs the gate depolarization chance.

The starting point contains a simulation setup where Alice prepares a qubit in a desired state.
The `application.py` file contains two methods `prepare_teleportation_qubit` and `calculate_fidelity_qubit`.
These methods contain functionality that is required for this exercise, but creating that code is not part of the exercise.

The rest of this README file will provide more detailed breakdown of the steps required for the exercise.


Implementing teleportation
------------------------------
The goal in this exercise is to implement the teleportation circuit that is shown in `Teleportation circuit.png`.

Steps in the AliceProtocol
=============================
1) Alice needs to generate a qubit that is entangled with a qubit a qubit on Bob. Use the `epr_socket` object for this.
2) Alice needs to apply a `cnot` gate with the teleportation qubit and the epr qubit.
3) Alice needs to apply a `H` gate to the teleportation qubit.
4) Alice needs to measure both qubits.
5) Alice needs to send send the measurement outcomes to bob. Use the `csocket` object for this.

Steps in the BobProtocol
=============================
1) Bob needs to participate in the process of generating entanglement. Use the `epr_socket` object for this.
2) Bob needs to receive the messages that Alice sends.
3) Verify the simulation works up to here and print the messages that Bob receives.
4) Conditionally apply `X` and `Z` gates to Bob's qubit depending on the message results.
5) Print the density matrix of the state of Bob's qubit using the `get_qubit_state` method.
6) Verify that the teleportation works by running the simulation multiple times and
comparing the qubit state on Alice's side with the qubit on Bob's side.
Also vary the variables `theta` and `phi` in `run_simulation.py`.

Plot gate depolarization chance vs fidelity for teleportation routine
--------------------------------------------------------------------------
The goal in this section is to create a plot of depolarization chance vs fidelity for the routine that was created in the previous exercise.
To achieve this we have to do three main actions:
1) Make each simulation return the fidelity of the generated qubit.
2) Make a `for loop` over simulation runs that changes the network configuration in each simulation run.
3) Put both the depolarization chance and fidelity results in lists and plot these lists.

Fidelity result return
========================
1) Add an `__init__` method to the BobProtocol that accepts and stores `theta` and `phi`.
2) Add the `theta` and `phi` arguments to the creation of th BobProtocol instance in `run_simulation.py`.
3) use the `calculate_fidelity_qubit` method in `application.py` to calculate the fidelity at the end of the BobProtocol.
4) Return the calculated fidelity as a result from the BobProtocol `run` method.
5) Create a variable that accepts the results from the `run` function in `run_simulation.py`.
6) Print and unpack these results until you have the fidelity value (Not a list or dictionary containing the value).

Modify network configuration in a for loop
=============================================
1) In `run_simulation.py` create a list of values for gate depolarization probabilities from 0 to 0.25 with steps of 0.025.
2) Create a `for loop` over these values that contains the `run` method.
3) Make an empty list before the `for loop` and append the fidelity value to this list in each iteration of the `for loop`.
4) In the for loop make an instance of `GenericQDeviceConfig` using `GenericQDeviceConfig.perfect_config()`.
5) Set the value of the parameter `two_qubit_gate_depolar_prob` in this config from the value of the for loop.
6) Create two instances of `StackConfig` one with the `name` Alice and one with `name` Bob. Set `qdevice_typ="generic"` and `qdevice_cfg` is the config object from the previous step.
7) Replace the `stacks` in the `StackNetworkConfig` object with a list of the two stacks instances from the previous step.
8) Print the list of fidelities and values for gate depolarization and run the simulation to check that it works.

Plot
=======
1) Use the `pyplot.plot` method with the two lists of values as arguments.
2) Use the `pyplot.show` of `pyplot.savefig` methods to display or save your plot.

