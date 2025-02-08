import matplotlib.pyplot as plt
import numpy as np

# Data
num_transactions = [100, 500, 1000, 5000]
latency_ibft = [200, 220, 250, 300]
latency_pow = [1500, 1600, 1700, 1800]
throughput_ibft = [500, 480, 450, 400]
throughput_pow = [20, 18, 15, 10]

# Plot Throughput
plt.figure(figsize=(10, 6))
plt.plot(num_transactions, throughput_ibft, label="Throughput (IBFT)", marker='o')
plt.plot(num_transactions, throughput_pow, label="Throughput (PoW)", marker='o')
plt.title("Throughput vs Number of Transactions")
plt.xlabel("Number of Transactions")
plt.ylabel("Throughput (tx/sec)")
plt.legend()
plt.grid(True)
plt.show()


