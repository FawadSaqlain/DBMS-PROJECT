import matplotlib.pyplot as plt
import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Add nodes with labels
labels = {
    'Employee': 'Employee',
    'CounterMgt': 'Counter Management',
    'InventoryMgt': 'Inventory Management',
    'Receipt': 'Receipt',
    'Product': 'Product',
    'ReturnReceipt': 'Return Receipt',
    'Manager': 'Manager',
    'SalesReport': 'Sales Report',
    'CustomerDetails': 'Customer Details\n(Optional: Name, Email)'
}

G.add_nodes_from(labels.keys())

# Add edges with relationships
edges = [
    ('Employee', 'CounterMgt', 'Works at (1..*)'),
    ('CounterMgt', 'Receipt', 'Generates (1..*)'),
    ('Receipt', 'Product', 'Contains (1..*)'),
    ('Employee', 'InventoryMgt', 'Works at (1..*)'),
    ('InventoryMgt', 'Product', 'Manages (1..*)'),
    ('Receipt', 'CustomerDetails', 'Has (0..1)'),
    ('Receipt', 'ReturnReceipt', 'Has (0..*)'),
    ('ReturnReceipt', 'Product', 'References (1)'),
    ('ReturnReceipt', 'Receipt', 'References (1)'),
    ('Manager', 'Employee', 'Manages (1..*)'),
    ('Manager', 'SalesReport', 'Generates (1..*)'),
    ('SalesReport', 'Receipt', 'Based on (1..*)')
]

for edge in edges:
    G.add_edge(edge[0], edge[1], label=edge[2])

# Use shell layout to avoid overlap, but you can try others like 'kamada_kawai_layout' or 'planar_layout'
pos = nx.shell_layout(G)

plt.figure(figsize=(15, 10))

# Draw nodes with a specific color and shape
nx.draw_networkx_nodes(G, pos, node_size=3000, node_color='lightblue', node_shape='s')

# Draw labels for nodes
nx.draw_networkx_labels(G, pos, labels, font_size=10, font_family='sans-serif')

# Draw edges with a bit more space between them
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='grey', connectionstyle='arc3,rad=0.1')

# Draw edge labels with a bit more padding
edge_labels = {(edge[0], edge[1]): edge[2] for edge in edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=8, font_family='sans-serif', label_pos=0.3)

# Adding title and making sure to remove axes for better clarity
plt.title("Enhanced ERD using Matplotlib and NetworkX", fontsize=15)
plt.axis('off')

# Save and show plot
plt.savefig('/mnt/data/enhanced_erd_improved.png')
plt.show()
