# import matplotlib.pyplot as plt
# import numpy as np

# # Data
# num_transactions = [100, 200, 300, 400,500]
# Throughput_IBFT = [13895.4,33475.26,51953.33,71230.5,90980.29]
# Throughput_QBFT= [24539.25,51257.84,75122.09,97099.09,120105.4]
# Throughput_CLIQUE=[18282.29,38311.1,55985.61,72831.63,89257.38]


# # Plot Throughput
# plt.figure(figsize=(10, 6))
# plt.plot(num_transactions, Throughput_IBFT, label="Throughput (IBFT)", marker='o')
# plt.plot(num_transactions, Throughput_QBFT, label="Throughput (QBFT)", marker='o')
# plt.plot(num_transactions, Throughput_CLIQUE, label="Throughput (CLIQUE)", marker='o')
# plt.title("Throughput vs Number of Transactions")
# plt.xlabel("Number of Transactions")
# plt.ylabel("Throughput (tx/sec)")
# plt.legend()
# plt.grid(True)
# plt.show()



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file
df = pd.read_csv("benchmark_result (1).csv")

# Group data by Algorithm and Number of Transactions (txnID), summing Throughput
df_throughput = df.groupby(["Algorithm", "txnID"]).agg({"Throughput(TPS)": "sum"}).reset_index()

# Compute cumulative sum of Throughput for each Algorithm
df_throughput["Cumulative Throughput(TPS)"] = df_throughput.groupby("Algorithm")["Throughput(TPS)"].cumsum()

# Plot Throughput vs. Number of Transactions for different Consensus Algorithms
plt.figure(figsize=(12, 6))
sns.lineplot(x="txnID", y="Cumulative Throughput(TPS)", hue="Algorithm", data=df_throughput, linestyle="-")

# Labels and title
plt.xlabel("Number of Transactions")
plt.ylabel("Cumulative Throughput (TPS)")
plt.title("Cumulative Throughput vs. Number of Transactions for Different Consensus Algorithms")
plt.legend(title="Consensus Algorithm")
plt.grid(True)

# Show the plot
plt.show()

# Print total sum of throughput for each Algorithm
total_throughput = df_throughput.groupby("Algorithm")["Cumulative Throughput(TPS)"].max()
print("Total Throughput for Each Algorithm:")
print(total_throughput)



