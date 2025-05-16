import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as ticker
import numpy as np



mpl.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['font.size'] = 12
mpl.rcParams['font.weight'] = 'bold'
mpl.rcParams['lines.linewidth'] = 1.5

# Config
base_dir = 'Get'
algorithms = ['Clique', 'IBFT', 'QBFT']
transactions = ['1000', '2000', '3000', '4000', '5000']
node_counts = ['5 Nodes','10 Nodes','15 Nodes', '20 Nodes', '25 Nodes']

for algo in algorithms:
    throughput_by_node = {node: [] for node in node_counts}

    for node in node_counts:
        folder_path = os.path.join(base_dir, node, algo)
        for txn in transactions:
            throughput = None
            for file in os.listdir(folder_path):
                if file.endswith('.csv') and txn in file:
                    df = pd.read_csv(os.path.join(folder_path, file))
                    throughput = df['Throughput(TPS)'].max()
                    break
            throughput_by_node[node].append(throughput)

    # Plot for this algorithm
    def power_formatter(x, pos):
        if x is None or np.isnan(x) or x == 0:
            return "0"
        exponent = int(np.floor(np.log10(abs(x))))
        coefficient = x / (10 ** exponent)
        return f'{coefficient:.1f}×10^{exponent}'

    scaling_factor = 1e5
    plt.figure(figsize=(5, 4))
    for node in node_counts:
        y_vals = [y / scaling_factor if y is not None else None for y in throughput_by_node[node]]
        plt.plot([int(txn) for txn in transactions], y_vals,linestyle='--', marker='o', label=node.replace('Nodes', ' Nodes'))

    #plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(power_formatter))
    plt.title(f'Max Throughput vs Number of Transactions ({algo})',fontsize=12, fontweight='bold')
    plt.xlabel('Number of Transactions',fontsize=12, fontweight='bold')
    plt.ylabel('Max Throughput (×10⁵ TPS)',fontsize=12, fontweight='bold')
    plt.legend(
    title='Node Count',
    loc='best',
    
    # fontsize=6,
    frameon=True,
    title_fontsize=10,
    prop={'size': 10, 'weight': 'bold'})
    plt.grid(True,linestyle='--')
    plt.xlim(900, 5100)
    plt.xticks(range(1000, 6000, 1000))
    plt.tight_layout()
    plt.show()
