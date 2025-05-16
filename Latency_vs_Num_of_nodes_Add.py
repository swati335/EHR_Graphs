import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# Base folder
base_folder = "Get"

# Parameters
transaction_counts = [1000, 2000, 3000, 4000, 5000]
node_counts = [10, 20, 25]
algorithms = ['Clique', 'IBFT', 'QBFT']
colors = {'Clique': '#1f77b4', 'IBFT': '#ff7f0e', 'QBFT': '#2ca02c'}

# Data container
latency_data = defaultdict(lambda: defaultdict(dict))  # txn -> algo -> node -> latency

# Load data
for node in node_counts:
    node_folder = f"{node}Node"
    for algo in algorithms:
        algo_folder = os.path.join(base_folder, node_folder, algo)
        if not os.path.exists(algo_folder):
            continue
        for file in os.listdir(algo_folder):
            if file.endswith(".csv") and "add" in file.lower():
                txn = int(file.split("_")[-1].replace(".csv", ""))
                if txn not in transaction_counts:
                    continue
                df = pd.read_csv(os.path.join(algo_folder, file))
                if "Latency(ms)" in df.columns:
                    avg_latency = df["Latency(ms)"].mean()
                    latency_data[txn][algo][node] = avg_latency

# 📊 Plotting: One plot per transaction count
fig, axes = plt.subplots(nrows=5, ncols=1, figsize=(10, 25), sharex=True)
fig.suptitle("⏱️ Latency vs Number of Nodes for Each Transaction Count", fontsize=18, fontweight='bold')

for idx, txn in enumerate(transaction_counts):
    ax = axes[idx]
    ax.set_title(f"📦 Transactions: {txn}", fontsize=14, fontweight='semibold')
    for algo in algorithms:
        nodes = sorted(latency_data[txn][algo].keys())
        latencies = [latency_data[txn][algo][n] for n in nodes]
        ax.plot(nodes, latencies, label=algo, color=colors[algo],
                marker='o', linewidth=2.5, markersize=6, markeredgecolor='black')

    ax.set_ylabel("Latency (ms)", fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend(title="Algorithm", fontsize=10, title_fontsize=11)

axes[-1].set_xlabel("Number of Nodes", fontsize=12)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()
