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

# Store average throughput for each algorithm
throughput_comparison = {'Add': [], 'Get': []}

for algo in algorithms:
    add_throughputs = []
    get_throughputs = []

    for node in node_counts:
        for txn in transactions:
            # Add
            path_add = os.path.join(base_dir_add, node, algo)
            for file in os.listdir(path_add):
                if file.endswith('.csv') and txn in file:
                    try:
                        df = pd.read_csv(os.path.join(path_add, file))
                        add_throughputs.append(df['Throughput(TPS)'].max())
                    except Exception as e:
                        print(f"Error reading Add file: {file} - {e}")
                    break

            # Get
            path_get = os.path.join(base_dir_get, node, algo)
            for file in os.listdir(path_get):
                if file.endswith('.csv') and txn in file:
                    try:
                        df = pd.read_csv(os.path.join(path_get, file))
                        get_throughputs.append(df['Throughput(TPS)'].max())
                    except Exception as e:
                        print(f"Error reading Get file: {file} - {e}")
                    break

    # Average of max throughput values
    throughput_comparison['Add'].append(max(add_throughputs))
    throughput_comparison['Get'].append(max(get_throughputs) )

# Plot
x = range(len(algorithms))
bar_width = 0.30
gap = 0.005 # Gap between bars

scaling_factor = 1e5


add_scaled = [val / scaling_factor for val in throughput_comparison['Add']]
get_scaled = [val / scaling_factor for val in throughput_comparison['Get']]

def power_formatter(x, pos):
    if x is None or np.isnan(x) or x == 0:
        return "0"
    # exponent = int(np.floor(np.log10(abs(x)))
    exponent=5
    coefficient = x / (10 ** exponent)
    return coefficient

plt.figure(figsize=(6,5))

add_positions = [i - (bar_width / 2 + gap / 2) for i in x]
get_positions = [i + (bar_width / 2 + gap / 2) for i in x]

add_bars = plt.bar(add_positions, throughput_comparison['Add'], width=bar_width, label='Add', color='goldenrod')
get_bars = plt.bar(get_positions, throughput_comparison['Get'], width=bar_width, label='Query', color='darkred')

# Add data labels on top of bars
for bar in add_bars + get_bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height , f'{height:.1f}', ha='center', va='bottom', fontsize=9,fontweight='bold')

# Styling

plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(power_formatter))
plt.xticks(ticks=x, labels=algorithms)
plt.xlabel('Consensus Algorithms',fontsize=12, fontweight='bold')
plt.ylabel('Max Throughput (×10⁵ TPS)',fontsize=12, fontweight='bold')
plt.title('Throughput Comparison: Add Data vs Query Data for Each Algorithm',fontsize=12, fontweight='bold')
plt.legend()
plt.grid(True, axis='y', linestyle='None', alpha=0.6)


plt.tight_layout()
plt.show()
