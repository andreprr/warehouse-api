from basic_lfsr import BasicLFSR
from general_lfsr import GeneralLFSR


def test_basic_lfsr():
    print("=== Basic LFSR Test ===")
    lfsr = BasicLFSR(initial_state="0110")
    for i in range(20):
        bit = lfsr.next_bit()
        print(f"{i+1:>2}: State: {lfsr.get_state()} | Output: {bit}")
    print()


def test_general_lfsr():
    print("=== General LFSR Test ===")
    lfsr = GeneralLFSR(size=4, taps=[0, 3])  # Misalnya tap di bit-0 dan bit-3
    lfsr.set_state("0110")
    for i in range(20):
        bit = lfsr.next_bit()
        print(f"{i+1:>2}: State: {lfsr.get_state()} | Output: {bit}")
    print()


def compare_streams():
    print("=== Comparing Output ===")
    basic = BasicLFSR(initial_state="0110")
    general = GeneralLFSR(size=4, taps=[0, 3])
    general.set_state("0110")

    match = True
    for i in range(20):
        b = basic.next_bit()
        g = general.next_bit()
        print(f"{i+1:>2}: Basic={b}, General={g}")
        if b != g:
            match = False

    if match:
        print("✅ Streams match!")
    else:
        print("❌ Streams do NOT match.")


if __name__ == "__main__":
    test_basic_lfsr()
    test_general_lfsr()
    compare_streams()
