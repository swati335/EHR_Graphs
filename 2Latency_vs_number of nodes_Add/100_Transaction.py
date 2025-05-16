# import os
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib as mpl
# import matplotlib.ticker as ticker
# import numpy as np

# mpl.rcParams['font.family'] = 'Times New Roman'
# mpl.rcParams['font.size'] = 14
# mpl.rcParams['font.weight'] = 'bold'
# mpl.rcParams['lines.linewidth'] = 3
# # mpl.rcParams['font.titleweight']='bold'

# # Set your base directory
# base_dir = 'Get'
# algorithms = ['Clique', 'IBFT', 'QBFT']
# node_counts = [ '5Node','10Node', '20Node', '25Node']
# transaction_count = '2000'

# # Dictionary to hold latency data
# latency_data = {algo: [] for algo in algorithms}

# # Extract latency for 1000 transactions
# for algo in algorithms:
#     for node in node_counts:
#         folder_path = os.path.join(base_dir, node, algo)
#         if not os.path.exists(folder_path):
#             latency_data[algo].append(None)
#             continue

#         latency = None
#         for file in os.listdir(folder_path):
#             if file.endswith('.csv') and transaction_count in file:
#                 df = pd.read_csv(os.path.join(folder_path, file))
#                 latency = df['Latency(ms)'].max()
#                 break

#         latency_data[algo].append(latency)

# # Plotting
# plt.figure(figsize=(12, 8))
# for algo in algorithms:
#     plt.plot([int(n.replace('Node', '')) for n in node_counts], latency_data[algo],linestyle='--',
#              marker='o', label=algo)

# plt.title('Latency vs Number of Nodes for 1000 Transactions',fontweight='bold')
# plt.xlabel('Number of Nodes',fontweight='bold')
# plt.ylabel('Latency (ms)',fontweight='bold')

# def power_formatter(x, pos):
#     # Avoid divide by zero error when x is 0
#     if x == 0:
#         return '0*10^0'  # Special case for zero
    
#     # Find the exponent
#     exponent = int(np.log10(x))
#     coefficient = x / (10 ** exponent)
    
#     # Format the coefficient to one decimal place and create the scientific notation
#     return f'{coefficient:.1f}x10^{exponent}'
# plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(power_formatter))

# plt.legend(
#     title='Algorithms',
#     loc='upper left',
#     fontsize=16,
#     title_fontsize=16,
#     frameon=True,
#     borderpad = 1.5
# )
# plt.grid(True, linestyle='--')
# plt.xlim(1, 26)
# plt.xticks(range(1, 26, 1)) 
# plt.tight_layout()
# plt.show()

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as ticker
import matplotlib.ticker as mticker
import numpy as np

# Matplotlib Settings
mpl.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['font.size'] = 12
mpl.rcParams['font.weight'] = 'bold'
mpl.rcParams['lines.linewidth'] = 1.5

# Configuration
base_dir = 'Get'
algorithms = ['Clique', 'IBFT', 'QBFT']
node_counts = ['5 Nodes', '10 Nodes','15 Nodes', '20 Nodes', '25 Nodes']
transaction_count = '5000'

# Dictionary to hold latency data
latency_data = {algo: [] for algo in algorithms}
missing_files = []  # To store missing file information

# Extract latency for given transactions
scaling_factor = 1e5
for algo in algorithms:
    for node in node_counts:
        folder_path = os.path.join(base_dir, node, algo)
        if not os.path.exists(folder_path):
            print(f"Warning: Folder not found - {folder_path}")
            latency_data[algo].append(None)
            continue

        latency = None
        for file in os.listdir(folder_path):
            if file.endswith('.csv') and transaction_count in file:
                df = pd.read_csv(os.path.join(folder_path, file))
                latency = df['Latency(ms)'].max()
                break  # Stop after finding the correct file

        if latency is None:
            missing_files.append((algo, node, transaction_count))
        
        latency_data[algo].append(latency)

# Show Missing Files Summary
if missing_files:
    print("\nMissing CSV files:")
    for algo, node, txn in missing_files:
        print(f" - Algorithm: {algo}, Node: {node}, Transactions: {txn}")
else:
    print("\nNo missing files found. ✅")

# Define custom formatter
def power_formatter(x, pos):
    if x is None or np.isnan(x) or x == 0:
        return "0"
    exponent = int(np.floor(np.log10(abs(x))))
    coefficient = x / (10 ** exponent)
    return f'{coefficient:.1f}×10^{exponent}'

# Plotting
plt.figure(figsize=(5, 4))
for algo in algorithms:
    x_vals = [int(n.replace('Nodes', '')) for n in node_counts]
    y_vals = [y / scaling_factor if y is not None else None for y in latency_data[algo]]
    plt.plot(
        x_vals, 
        y_vals, 
        linestyle='--',
        marker='o',
        label=algo,
        zorder=2
    )

plt.title(f'Max Latency vs Number of Nodes for {transaction_count} Transactions',fontsize=12, fontweight='bold')
plt.xlabel('Number of Nodes',fontsize=12, fontweight='bold')
plt.ylabel('Max Latency (×10⁵ ms)',fontsize=12, fontweight='bold')

# plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(power_formatter))

legend =plt.legend(
    title='Algorithms',
    loc='upper right',
    fontsize=10,
    title_fontsize=10,
    frameon=True,
    bbox_to_anchor=(1.005, 1.0),
    # borderpad=1.0
)
legend.set_zorder(1.5)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlim(4, 28)
plt.xticks(range(5, 26, 5))
# plt.yticks(range(0.0 , 1.0,0.2))
plt.tight_layout()
plt.show()

