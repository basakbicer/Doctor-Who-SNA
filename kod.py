import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network




# Define the file path
file_path =  r"C:\Users\Casper\OneDrive - bandirma.edu.tr\Masaüstü\son.csv"

# Read the data from the CSV file
data = pd.read_csv(file_path)

# Networkx için bir graf oluştur
G = nx.from_pandas_edgelist(data, 'Source', 'Target', ['Weight', 'Type'])

# Düğümlerin bağlantı sayılarını içeren bir sözlük oluştur
node_degrees = dict(G.degree())


degree_centrality = dict(G.degree())
betweenness_centrality = dict(nx.betweenness_centrality(G,weight ="Weight"))
closeness_centrality = dict(nx.closeness_centrality(G))

#kümelenme katsayısı
clustering_coefficients = nx.clustering(G)
for node, cc in clustering_coefficients.items():
    print(f"Node {node}: Clustering Coefficient = {cc}")


# Bağlı bileşenleri bul
connected_components = list(nx.connected_components(G))

# Graf özelliklerini hesaplamak için boş listeler oluştur
node_counts = []
edge_counts = []
densities = []
diameters = []
avg_shortest_path_lengths = []

# Her bir bağlı bileşen üzerinde işlem yapabilirsiniz
for i, component in enumerate(connected_components):
    subgraph = G.subgraph(component)
    
    # Graf özelliklerini hesapla
    node_counts.append(subgraph.number_of_nodes())
    edge_counts.append(subgraph.number_of_edges())
    densities.append(nx.density(subgraph))
    # Derece dağılımlarını hesapla
    degree_sequence = sorted([d for n, d in subgraph.degree()], reverse=True)
    degree_count = nx.degree_histogram(subgraph)
    degrees = range(len(degree_count))

    # Derece dağılımını grafiğe çiz
    plt.bar(degrees, degree_count, width=0.80, color='b', alpha=0.5, label=f'Component {i + 1}')
    
    
    
    try:
        diameter = nx.diameter(subgraph)
        avg_shortest_path_length = nx.average_shortest_path_length(subgraph)
    except nx.NetworkXError:
        diameter = "N/A"
        avg_shortest_path_length = "N/A"
    
    diameters.append(diameter)
    avg_shortest_path_lengths.append(avg_shortest_path_length)



# Ara merkezilik değerlerini ağırlıklı olarak hesapla
betweenness_centrality = dict(nx.betweenness_centrality(G, weight='Weight'))

# betweenness centrality değerlerini yazdır
for node, bc in betweenness_centrality.items():
    print(f"Node {node}: Betweenness Centrality = {bc}")


# Sonuçları yazdır
for i, component in enumerate(connected_components):
    print(f"Component {i + 1}:")
    print(f"  Düğüm Sayısı: {node_counts[i]}")
    print(f"  Kenar Sayısı: {edge_counts[i]}")
    print(f"  Yoğunluk: {densities[i]}")
    print(f"  Çap: {diameters[i]}")
    print(f"  Ortalama Yol Uzunluğu: {avg_shortest_path_lengths[i]}")
    print()

plt.title("Bağlı Bileşenler Üzerinde Derece Dağılımları")
plt.xlabel("Derece")
plt.ylabel("Düğüm Sayısı")
plt.legend()
plt.show()
    
# Düğümlerin boyutlarını belirle
node_sizes = [5* node_degrees[node] for node in G.nodes]

#label belirle
edge_labels = {('Amy Pond', 'Eleventh Doctor'): '+', ('Clara Oswald', 'Eleventh Doctor'): '+'}



# Grafı çiz
pos = nx.random_layout(G)
#nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color='skyblue', font_size=8, font_color='black', font_weight='bold', edge_color='gray', linewidths=1.5, alpha=0.7)

# Grafik üzerine bağlantı işaretlerini ekleyin
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.2)

net= Network(notebook=True)
net.force_atlas_2based()

#net.from_networkx(G, node_size=node_sizes, node_color='skyblue', font_size=8, font_color='black', font_weight='bold', edge_color='gray', linewidths=1.5, alpha=0.7)
net.add_nodes(G.nodes)
net.add_edges(G.edges)

# Set node sizes directly in the 'nodes' attribute
for i, node in enumerate(G.nodes):
    net.nodes[i]['size'] = node_sizes[i]

net.show_buttons()
net.set_edge_smooth('dynamic')

'''
for idx, (edge, label) in enumerate(edge_labels.items()):
    src, target = edge
    net.edges[idx]['label'] = label

   '''

net.from_nx(G)
net.show("doctorwho.html")



import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def clique_percolation(graph, k):
    cliques = [frozenset(clique) for clique in nx.find_cliques(graph) if len(clique) == k]
    communities = []
    
    while cliques:
        current_clique = cliques.pop(0)
        new_community = set(current_clique)
        
        neighbors = set.union(*(set(graph.neighbors(node)) for node in current_clique))
        candidate_cliques = [frozenset(clique) for clique in cliques if len(clique.intersection(neighbors)) >= k - 1]
        
        while candidate_cliques:
            candidate = candidate_cliques.pop(0)
            if len(candidate.intersection(neighbors)) >= k - 1:
                new_community.update(candidate)
                neighbors = set.union(neighbors, set.union(*(set(graph.neighbors(node)) for node in candidate)))
                cliques = [clique for clique in cliques if clique not in candidate_cliques]
                candidate_cliques = [clique for clique in candidate_cliques if not candidate.intersection(clique)]
        
        communities.append(new_community)
    
    return communities

# CPM uygula ve toplulukları bul
k_value = 3
communities = clique_percolation(G, k_value)

# Toplulukları görselleştir
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G)

for i, community in enumerate(communities):
    nx.draw_networkx_nodes(G, pos, nodelist=community, node_color=f'C{i}', node_size=200)

edges = G.edges()
nx.draw_networkx_edges(G, pos, edgelist=edges, width=1.0, alpha=0.5, edge_color='gray')

plt.title("Clique Percolation Method ile Topluluklar")
plt.show()



# Jaccard benzerliğini hesaplayan fonksiyon
def jaccard_similarity(graph, node1, node2):
    neighbors1 = set(graph.neighbors(node1))
    neighbors2 = set(graph.neighbors(node2))
    intersection = neighbors1.intersection(neighbors2)
    union = neighbors1.union(neighbors2)
    return len(intersection) / len(union)

# PathSim benzerliğini hesaplayan fonksiyon
def path_similarity(graph, node1, node2):
    try:
         shortest_path_length = nx.shortest_path_length(graph, source=node1, target=node2)
         return 1 / (1 + shortest_path_length)
    except nx.NetworkXNoPath:
        return 0  # Return 0 if there is no path between nodes



# Jaccard benzerliklerini hesapla ve yazdır
for node1 in G.nodes:
    for node2 in G.nodes:
        if node1 != node2:
            jaccard_similarity_result = jaccard_similarity(G, node1, node2)  # Değişken adını değiştirdik
            path_similarity_result = path_similarity(G, node1, node2)
            if jaccard_similarity_result > 0:  # Sadece sıfır olmayanları yazdır
                # print(f"Jaccard similarity between {node1} and {node2}: {jaccard_similarity_result:.4f}")

                 print(f"PathSim between {node1} and {node2}: {path_similarity_result:.4f}")
                 




                 