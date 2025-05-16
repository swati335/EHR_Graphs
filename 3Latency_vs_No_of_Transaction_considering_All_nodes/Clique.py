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
node_counts = [ '5 Nodes','10 Nodes','15 Nodes', '20 Nodes', '25 Nodes']
# line_styles = [':', '--', '-', '-.']
for algo in algorithms:
    latency_by_node = {node: [] for node in node_counts}

    for node in node_counts:
        folder_path = os.path.join(base_dir, node, algo)
        for txn in transactions:
            latency = None
            for file in os.listdir(folder_path):
                if file.endswith('.csv') and txn in file:
                    df = pd.read_csv(os.path.join(folder_path, file))
                    latency = df['Latency(ms)'].max()
                    break
            latency_by_node[node].append(latency)

    # Plot for this algorithm
    def power_formatter(x, pos):
        if x is None or np.isnan(x) or x == 0:
            return "0"
        exponent = int(np.floor(np.log10(abs(x))))
        coefficient = x / (10 ** exponent)
        return f'{coefficient:.1f}×10^{exponent}'


    scaling_factor = 1e5
    plt.figure(figsize=(5, 4))
    colors = ['darkred', 'darkorange', 'darkgreen', 'royalblue', 'goldenrod']
    for idx, node in enumerate(node_counts):
        # style = line_styles[idx % len(line_styles)]
        y_vals = [y / scaling_factor if y is not None else None for y in latency_by_node[node]]
        plt.plot(
            [int(txn) for txn in transactions],
            y_vals,
            linestyle='--',
            marker='o',
            color=colors[idx % len(colors)],
            label=node.replace('Nodes', ' Nodes'),
            zorder=2
        )

    plt.title(f'Max Latency vs Number of Transactions ({algo})',fontsize=12, fontweight='bold')
    plt.xlabel('Number of Transactions',fontsize=12, fontweight='bold')
    plt.ylabel('Max Latency (×10⁵ ms)',fontsize=12, fontweight='bold')
    
    #plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(power_formatter))
    legend=plt.legend(
    title='Node Count',
    loc='best',
    
    # fontsize=6,
    frameon=True,
    title_fontsize=10,
    prop={'size': 10, 'weight': 'bold'}
    # borderpad=1.1
     )
    legend.set_zorder(1.5)
    # plt.tight_layout(rect=[0, 0, 0.8, 1]) 
    plt.grid(True,linestyle='--')
    plt.xlim(500, 5100)
    plt.xticks(range(1000, 6000, 1000))
    # plt.tight_layout(rect=[0, 0, 0.85, 1])
    plt.show()
