import subprocess
import glob
import numpy as np
import re
import matplotlib.pyplot as plt
import argparse
from sklearn.cluster import AgglomerativeClustering
from sklearn.neighbors import NearestCentroid
from sklearn.metrics import pairwise_distances

#function tho compute the RMSD
def calculate_rmsd(file1, file2):
    """Calculate TM-score between two protein structure files."""
    # Command to run TM-score program
    cmd = f"./TMscore -split 1 -ter 0 {file1} {file2} -seq | grep RMSD"

 # Run command and capture output
    output = subprocess.check_output(cmd, shell=True)
    print(output)
    rmsd = re.search(r'\d+\.\d+', output.decode()).group()
    rmsd=float(rmsd)
    print(rmsd)
    return rmsd

#Ask for the required arguments
parser=argparse.ArgumentParser(description='Program description')
parser.add_argument('--path_exp', required='True', help='Path of the experimental files')
parser.add_argument('--out_file', required='True', help='List of non-rdundant experimental structures')
args=parser.parse_args()

out_file=args.out_file
path_to_exp=args.path_exp
exp_files = glob.glob(path_to_exp + '/*.pdb')

num_exp=len(exp_files)

#Compute the RMSD between all the experimental structures
rmsd_experimental_structures=np.zeros((num_exp, num_exp))
for i in range(num_exp):
        for j in range(num_exp):
            rmsd_experimental_structures[i][j] = calculate_rmsd(exp_files[i], exp_files[j])

#Cluster the structures by a distance of 2 A
clusters_agg = AgglomerativeClustering(n_clusters=None, distance_threshold=2, compute_full_tree=True, metric='precomputed', linkage='average').fit_predict(rmsd_experimental_structures)
print(clusters_agg)

# Find the centroids
unique_labels = np.unique(clusters_agg)
centroids = []
for label in unique_labels:
    cluster_indices = np.where(clusters_agg == label)[0]
    centroid = np.mean(rmsd_experimental_structures[cluster_indices], axis=0)
    centroids.append(centroid)

# Find the nearest protein to each centroid
nearest_proteins = []
for centroid in centroids:
    distances_to_centroid = np.linalg.norm(rmsd_experimental_structures - centroid, axis=1)
    nearest_idx = np.argmin(distances_to_centroid)
    nearest_protein = nearest_idx  # This should be your protein index in your dataset
    nearest_proteins.append(nearest_protein)

print("Nearest protein indices to centroids:", nearest_proteins)

#Write the centroids (representative structures) in a file
file_out_list=open(out_file+'.txt', 'wt')
for i in nearest_proteins:
	file_out_list.write(exp_files[i]+ '\n')

file_out_list.close()

np.save(out_file, rmsd_experimental_structures)

plt.title(out_file)
plt.imshow(rmsd_experimental_structures, aspect='auto')
plt.xlabel('Experimental structures')
plt.ylabel('Experimental structures')
plt.colorbar()
plt.tight_layout()
plt.show()