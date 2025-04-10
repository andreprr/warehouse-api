class BasicLFSR:
    def __init__(self, initial_state: str = "0110"):
        self.state = [int(bit) for bit in initial_state]

    def get_state(self) -> str:
        return ''.join(str(bit) for bit in self.state)

    def next_bit(self) -> int:
        # Tap hardcoded: XOR bit ke-0 dan ke-3 (index 0 dan 3)
        feedback = self.state[0] ^ self.state[3]
        output = self.state[0]

        # Shift left dan masukkan feedback di ujung
        self.state = self.state[1:] + [feedback]
        return output
