import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as ticker
import numpy as np
from collections import defaultdict

mpl.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['font.size'] = 12
mpl.rcParams['font.weight'] = 'bold'
mpl.rcParams['lines.linewidth'] = 1.5

# === SETTINGS ===
base_folder = "Get"
transaction_counts = [1000, 2000, 3000, 4000, 5000]
node_counts = [5,10,15,20, 25]
algorithms = ['Clique', 'IBFT', 'QBFT']  # Adjust if you want to pick only one
selected_algo = 'IBFT'  # Example: only plot for Clique

# Colors for each transaction count
colors = {
    1000: 'darkred',
    2000: 'darkorange',
    3000: 'darkgreen',
    4000: 'royalblue',
    5000: 'goldenrod'
}

# === DATA COLLECTION ===
throughput_by_txn = defaultdict(dict)  # txn -> {node: latency}

for node in node_counts:
    node_folder = f"{node} Nodes"
    algo_folder = os.path.join(base_folder, node_folder, selected_algo)
    if not os.path.exists(algo_folder):
        continue

    for file in os.listdir(algo_folder):
        if file.endswith(".csv") and "get" in file.lower():
            txn = int(file.split("_")[-1].replace(".csv", ""))
            if txn not in transaction_counts:
                continue
            df = pd.read_csv(os.path.join(algo_folder, file))
            if "Throughput(TPS)" in df.columns:
                avg_throughput = df["Throughput(TPS)"].max()
                throughput_by_txn[txn][node] = avg_throughput

# === PLOTTING ===

def power_formatter(x, pos):
    if x is None or np.isnan(x) or x == 0:
        return "0"
    # exponent = int(np.floor(np.log10(abs(x))))
    exponent=5
    coefficient = x / (10 ** exponent)
    return coefficient

plt.figure(figsize=(6,5))
for txn in transaction_counts:
    data = throughput_by_txn[txn]
    nodes = sorted(data.keys())
    throughtputs = [data[n] for n in nodes]
    plt.plot(nodes, throughtputs, label=f"{txn} txns", color=colors[txn],linestyle='--',
             marker='o', linewidth=2.5, markersize=6, markeredgecolor='black')

plt.title(f"Max Throughput vs Number of Nodes ({selected_algo})", fontsize=12, fontweight='bold')
plt.xlabel("Number of Nodes", fontsize=12,fontweight='bold')
plt.ylabel("Max Throughput (×10⁵ TPS)",fontsize=12,fontweight='bold')

plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(power_formatter))

plt.grid(True, linestyle='--', alpha=0.4)
plt.legend(
    title="Transaction Count",
    loc='best',
    fontsize=10,
    title_fontsize=10,
    frameon=True,
    # borderpad=1.2
)
plt.xlim(4, 26)
plt.xticks(range(5, 26, 5))  
plt.tight_layout()
plt.show()
