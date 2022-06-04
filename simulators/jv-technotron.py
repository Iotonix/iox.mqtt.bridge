from interfaces.simulator_interface import SimulatorInterface


class Simulator(SimulatorInterface):
    def __init__(self):
        print("Plug initialized")

    def simulate(self, iteration):
        print("Simulating now", iteration)

    def terminate(self):
        print("Cleaning Up")