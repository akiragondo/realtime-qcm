from simulator.simulator import Simulator
from detectors.test_sim import AlgTester


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    algorithms = [
        AlgTester(sigma_thresh=6,initial_sample_size=1000)
    ]
    sim = Simulator(input_folder='.\data',data_packet_size=50)
    for algorithm in algorithms:
        sim.runDetector(algorithm=algorithm)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
