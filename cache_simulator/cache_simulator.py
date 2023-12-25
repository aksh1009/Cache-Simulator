class CacheSimulator:
    def __init__(self, cache_size, block_size, associativity):
        self.cache_size = cache_size
        self.block_size = block_size
        self.associativity = associativity
        self.num_blocks = cache_size // block_size
        self.cache = [[] for _ in range(self.num_blocks)]
        self.hits = 0
        self.misses = 0
        self.index_bits = self._log2(self.num_blocks // associativity)
        self.offset_bits = self._log2(block_size)

    def _log2(self, x):
        return (x.bit_length() - 1) if x > 0 else 0

    def _lru_update(self, index, tag):
        self.cache[index].remove(tag)
        self.cache[index].append(tag)

    def access_memory(self, address):
        word_address = address // 4
        binary_address = format(address, '032b')
        offset = int(binary_address[-self.offset_bits:], 2)
        index = int(binary_address[-(self.offset_bits + self.index_bits):-self.offset_bits], 2)
        tag = binary_address[:-self.offset_bits]

        if tag in self.cache[index]:
            self.hits += 1
            self._lru_update(index, tag)
        else:
            self.misses += 1
            if len(self.cache[index]) < self.associativity:
                self.cache[index].append(tag)
            else:
                self.cache[index].pop(0)
                self.cache[index].append(tag)

    def simulate_memory_accesses(self, memory_accesses):
        for address, _ in memory_accesses:
            self.access_memory(address)

    def print_stats(self):
        print("\n" + "-" * 60)
        print("Simulation Statistics")
        print(f"Cache Size: {self.cache_size} bytes")
        print(f"Block Size: {self.block_size} bytes")
        print(f"Associativity: {self.associativity}")
        print(f"Number of Blocks: {self.num_blocks}")
        print(f"Number of Hits: {self.hits}")
        print(f"Number of Misses: {self.misses}")

        # Calculate and display hit rate only if there are hits and misses
        if self.hits + self.misses > 0:
            hit_rate = self.hits / (self.hits + self.misses) * 100
            print(f"Hit Rate: {hit_rate:.2f}%")
        else:
            print("Hit Rate: N/A")

# Example usage:
cache_simulator = CacheSimulator(cache_size=64, block_size=8, associativity=2)
memory_accesses = [
    (0x0A, "R"),
    (0x0B, "R"),
    (0x0C, "R"),
    (0x0D, "R"),
    (0x0E, "R"),
    (0x0F, "R"),
    (0x10, "R"),
    (0x11, "R"),
    (0x12, "R"),
    (0x13, "R"),
    (0x14, "R"),
]

cache_simulator.simulate_memory_accesses(memory_accesses)
cache_simulator.print_stats()
