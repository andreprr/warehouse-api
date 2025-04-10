class GeneralLFSR:
    def __init__(self, size: int, taps: list[int]):
        self.size = size
        self.taps = taps  # misal [0, 3]
        self.state = [0] * size

    def set_state(self, state_str: str):
        if len(state_str) != self.size:
            raise ValueError("State length must match register size.")
        self.state = [int(bit) for bit in state_str]

    def get_state(self) -> str:
        return ''.join(str(bit) for bit in self.state)

    def next_bit(self) -> int:
        # XOR semua tap
        feedback = 0
        for i in self.taps:
            feedback ^= self.state[i]

        output = self.state[0]
        self.state = self.state[1:] + [feedback]
        return output
