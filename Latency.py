# import matplotlib.pyplot as plt
# import numpy as np


# num_transactions = [100, 200, 300, 400, 500]
# latency_IBFT = [982,1589,2274,2915,3585]
# latency_CLIQUE = [617,1178,1815,2497,3191]
# latency_QBFT=[455,887,1357,1867,2358]


# # Plot Latency
# plt.figure(figsize=(10, 6))
# plt.plot(num_transactions, latency_IBFT, label="Latency (IBFT)", marker='o')
# plt.plot(num_transactions, latency_QBFT, label="Latency (QBFT)", marker='o')
# plt.plot(num_transactions, latency_CLIQUE, label="Latency (CLIQUE)", marker='o')

# plt.title("Latency vs Number of Transactions")
# plt.xlabel("Number of Transactions")
# plt.ylabel("Latency (ms)")
# plt.legend()
# plt.grid(True)
# plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file
df = pd.read_csv("benchmark_result (1).csv")

# Group data by Algorithm and Number of Transactions (txnID), summing Latency
latency_by_txn = df.groupby(["Algorithm", "txnID"]).agg({"Latency(ms)": "sum"}).reset_index()

# Compute cumulative sum of Latency for each Algorithm
latency_by_txn["Cumulative Latency(ms)"] = latency_by_txn.groupby("Algorithm")["Latency(ms)"].cumsum()

# Plot Latency vs. Number of Transactions for different Consensus Algorithms
plt.figure(figsize=(12, 6))
sns.lineplot(x="txnID", y="Cumulative Latency(ms)", hue="Algorithm", data=latency_by_txn, linestyle="-")

# Labels and title
plt.xlabel("Number of Transactions")
plt.ylabel("Cumulative Latency (ms)")
plt.title("Cumulative Latency vs. Number of Transactions for Different Consensus Algorithms")
plt.legend(title="Consensus Algorithm")
plt.grid(True)

# Show the plot
plt.show()

# Print total sum of latency for each Algorithm
total_latency = latency_by_txn.groupby("Algorithm")["Cumulative Latency(ms)"].max()
print("Total Latency for Each Algorithm:")
print(total_latency)



