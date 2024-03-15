import numpy as np
from netqasm.sdk.classical_communication.socket import Socket
from netqasm.sdk.connection import BaseNetQASMConnection
from netqasm.sdk.epr_socket import EPRSocket
from netqasm.sdk.qubit import Qubit
from netsquid import sim_time
from netsquid.qubits import qubitapi

from squidasm.sim.stack.program import Program, ProgramContext, ProgramMeta
from squidasm.util import get_qubit_state


def prepare_teleportation_qubit(connection: BaseNetQASMConnection, theta: float = 0, phi: float = 0) -> Qubit:
    r"""This method prepares a qubit in the state:
     :math:`\cos(\theta / 2)|0\rangle + e^{i\phi}\sin(\theta / 2)|1\rangle`.

    :param connection: The connection to the QNPU.
    :param phi: Angle around Z-axis from X-axis
    :param theta: Angle from Z-axis
    :returns: A qubit in the desired state.
    """

    qubit = Qubit(connection)
    qubit.rot_Y(angle=theta)
    qubit.rot_Z(angle=phi)
    return qubit


def calculate_fidelity_qubit(dm_qubit_state: np.ndarray, theta: float, phi: float) -> float:
    r"""
    Calculates the fidelity between the state given via the density matrix and the state:
    :math:`\cos(\theta / 2)|0\rangle + e^{i\phi}\sin(\theta / 2)|1\rangle`.

    :param dm_qubit_state: The density matrix of the qubit
    :param phi: Angle around Z-axis from X-axis for the reference state.
    :param theta: Angle from Z-axis for the reference state.
    :returns: The fidelity.
    """
    qubit = qubitapi.create_qubits(1, "qubit")
    qubitapi.assign_qstate(qubit, dm_qubit_state)
    target_state = np.array([np.cos(theta / 2), np.sin(theta / 2) * np.exp(-1j * phi)])
    fid = qubitapi.fidelity(qubit, target_state, squared=True)
    return fid


class AliceProgram(Program):
    PEER_NAME = "Bob"

    def __init__(self, theta: float, phi: float):
        self.theta = theta
        self.phi = phi

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name="exercise_program",
            csockets=[self.PEER_NAME],
            epr_sockets=[self.PEER_NAME],
            max_qubits=10,
        )

    def run(self, context: ProgramContext):
        # Classical socket to Bob
        csocket = context.csockets[self.PEER_NAME]
        # EPR socket to Bob
        epr_socket = context.epr_sockets[self.PEER_NAME]
        # Connection to quantum network processing unit
        connection = context.connection

        # Use method above to create a qubit and rotate it to the desired state
        qubit = prepare_teleportation_qubit(connection, self.theta, self.phi)
        # Send the instructions to the QNPU, thereby causing Alice to prepare the qubit
        yield from connection.flush()
        # Make a snapshot of the state of the qubit. The node name must be specified due to technical limitations
        qubit_density_matrix = get_qubit_state(qubit, node_name="Alice")
        # Using the sim_time method from netsquid, we can retrieve the current time in the simulation in nanoseconds
        print(f"{sim_time()} ns, Alice prepares a qubit in state:\n{qubit_density_matrix}")

        return {}


class BobProgram(Program):
    PEER_NAME = "Alice"

    @property
    def meta(self) -> ProgramMeta:
        return ProgramMeta(
            name="exercise_program",
            csockets=[self.PEER_NAME],
            epr_sockets=[self.PEER_NAME],
            max_qubits=10,
        )

    def run(self, context: ProgramContext):
        # Classical socket to Alice
        csocket: Socket = context.csockets[self.PEER_NAME]
        # EPR socket to Alice
        epr_socket: EPRSocket = context.epr_sockets[self.PEER_NAME]
        # Connection to quantum network processing unit
        connection: BaseNetQASMConnection = context.connection

        return {}
