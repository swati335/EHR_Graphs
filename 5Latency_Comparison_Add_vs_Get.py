import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as ticker
import numpy as np

mpl.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['font.size'] = 12
mpl.rcParams['font.weight'] = 'bold'
mpl.rcParams['lines.linewidth'] = 3

# Configuration
base_dir_add = 'Add'
base_dir_get = 'Get'
algorithms = ['Clique', 'IBFT', 'QBFT']
node_counts = ['5 Nodes','10 Nodes','15 Nodes', '20 Nodes', '25 Nodes']
transactions = ['1000', '2000', '3000', '4000', '5000']

# Store average latency for each algorithm
latency_comparison = {'Add': [], 'Get': []}

for algo in algorithms:
    add_latencies = []
    get_latencies = []

    for node in node_counts:
        for txn in transactions:
            # Add
            path_add = os.path.join(base_dir_add, node, algo)
            for file in os.listdir(path_add):
                if file.endswith('.csv') and txn in file:
                    try:
                        df = pd.read_csv(os.path.join(path_add, file))
                        add_latencies.append(df['Latency(ms)'].max())
                    except Exception as e:
                        print(f"Error reading Add file: {file} - {e}")
                    break

            # Get
            path_get = os.path.join(base_dir_get, node, algo)
            for file in os.listdir(path_get):
                if file.endswith('.csv') and txn in file:
                    try:
                        df = pd.read_csv(os.path.join(path_get, file))
                        get_latencies.append(df['Latency(ms)'].max())
                    except Exception as e:
                        print(f"Error reading Get file: {file} - {e}")
                    break

    # Average of max latencies
    # latency_comparison['Add'].append(sum(add_latencies) / len(add_latencies))
    # latency_comparison['Get'].append(sum(get_latencies) / len(get_latencies))

    latency_comparison['Add'].append(max(add_latencies))
    latency_comparison['Get'].append(max(get_latencies))

# Plot
x = range(len(algorithms))
bar_width = 0.30
gap = 0.005  # Gap between bars


def power_formatter(x, pos):
    if x is None or np.isnan(x) or x == 0:
        return "0"
    # exponent = int(np.floor(np.log10(abs(x))))
    exponent=5
    coefficient = x / (10 ** exponent)
    return coefficient

plt.figure(figsize=(6, 5))
scaling_factor = 1e5


add_scaled = [val / scaling_factor for val in latency_comparison['Add']]
get_scaled = [val / scaling_factor for val in latency_comparison['Get']]

add_positions = [i - (bar_width / 2 + gap / 2) for i in x]
get_positions = [i + (bar_width / 2 + gap / 2) for i in x]

add_bars = plt.bar(add_positions, latency_comparison['Add'], width=bar_width, label='Add', color='goldenrod')
get_bars = plt.bar(get_positions, latency_comparison['Get'], width=bar_width, label='Query', color='darkred')

#Add data labels on top of bars
for bar in add_bars + get_bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.1f}', ha='center', va='bottom', fontsize=9,fontweight='bold')




# Styling

plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(power_formatter))
plt.xticks(ticks=x, labels=algorithms)
plt.xlabel('Consensus Algorithms',fontsize=12, fontweight='bold')
plt.ylabel('Max Latency (×10⁵ ms)',fontsize=12, fontweight='bold')
plt.title('Latency Comparison: Add Data vs Query Data for Each Algorithm',fontsize=12, fontweight='bold')
plt.legend(loc='best',
    fontsize=10,
    title_fontsize=10,
    frameon=True,)
plt.grid(True, axis='y', linestyle='None', alpha=0.6)
# plt.ylim(0, 10.5)
# plt.yticks(np.arange(0, 10.1, 1.0))  
# max_height = max(max(add_scaled), max(get_scaled))
# plt.ylim(0, max_height + 12)
# plt.yticks(np.arange(0, 10.1, 10000))  
plt.tight_layout()
plt.show()
