import matplotlib.pyplot as plt
import numpy as np


num_transactions = [100, 500, 1000, 5000]
latency_ibft = [200, 220, 250, 300]
latency_pow = [1500, 1600, 1700, 1800]


# Plot Latency
plt.figure(figsize=(10, 6))
plt.plot(num_transactions, latency_ibft, label="Latency (IBFT)", marker='o')
plt.plot(num_transactions, latency_pow, label="Latency (PoW)", marker='o')
plt.title("Latency vs Number of Transactions")
plt.xlabel("Number of Transactions")
plt.ylabel("Latency (ms)")
plt.legend()
plt.grid(True)
plt.show()