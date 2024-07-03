# TransAtlas_AF

Here are presented all the scripts developed for this project. The methods used by other authors are not included.

## AlphaFold running
First, there is an example of how to run AlphaFold (script named AF_run_example.sh). The variables needed to change are in this command line:
'''
python RunAF2multi.py /scratch/mmb/mromagosa/AFCluster/msas1DEG/EX_{101..150}.a3m --model_num 1 --recycles 3 --output_dir out1DEG --af2_dir /apps/alpha_fold
'''

## Experimental structures clsutering
The .py file is the one that makes AlphaFold run. The first argument are the MSAs that have to be introduced. This argument has to be changed depending on the MSAs that one wants to model. The other argument that needs to be changed is the --output_dir, which is where do the pdb files of the generated structure predictions get saved.

The script exp_filter.py clusters the experimental structures by similarity and gives as output a file with the file names of the representative structure of each cluster. The inputs needed are: '''--path_exp''' (path to the directory where the pdb of the experimental structures are saved) and '''--out_file''' (file where the representative structure names will be written).

## Quality factor
qmean.py makes a query to QMEAN to compute the qmean6 quality factor. The needed inputs are --path_AF, that is the directory of the AlphaFold generated structures, and --out_file, that is the file name where the results will be saved. This file contains 2 columns. The first one includes the file names of all processed pdbs and the second one is the computed qmean6 score.

## AF structures analysis
The file analysis_filter.py filters the structure with not enough quality, taking the data from the proviously explained file, computes the RMSD between all the AF-generated structures to later cluster them, get with the centroids as representative structures and discard the redundant structures. Later, the RMSD between all the AF-generated structures and the experimental structures is computed. This metric is used to determine if the protocol is able to reproduce the different experimentally solved conformations. This script gives as output figures of the all-to-all RMSD, the RMSD between the AF structures and the experimental structures when no filter is done, when the structures are filtered, when the structures are clustered and when the structures are filtered and clustered. There is also a file with lists about:
 - Before filtering by quality: all the AF-structures file name, the experimental structure file name that is closer to that AF-structure and the RMSD of the pair; all the experimental structures with its closest AF-structure and the RMSD of the pair; and the experimental structure with its closest centroid.
 - After filtering by quality, the same results are presented. 
 
 In all cases, the percentage of covered structures is presented (understanding covered as being the best pair for some structure).
 This script also gives as output a file with a list of the file names of the structures detemined to be the centroids of each cluster.
 
The needed arguments to use this file are: --path_AF (Path of the PDB files), --exp_list (Path to the file with the experimental representative structure names), --out_file (name of the file where all the mentioned information will be saved), --qmean_th (Threshold for the qmean filter), cluster_th (distance threshold for the cluster generation), qmean_file (file with the list of the pdb files and their qmean6 score). Some other not required arguments can be given. These are added when the RMSDs have already been generated and just other arguments are wanted to be changed, since the creation of the RMSD matrix is most computationally expensive part. The arguments are --rmsd (all-to-all rmsd in .npy format) and --rmsd_exp (rmsd between the AF-generated structures and the experimetnal structures).
 
## Trajectory generation
To compute the trajectories, it is needed to download the [workflow from biobb](https://mmb.irbbarcelona.org/biobb/workflows#protein-conformational-transitions-calculations). Then, the script I created named megaworkflow.py uploads the .yml file and runs the workflow.py file fore every needed trajectory. The program computes the trajectory between all the centroids. The file with a list of all centroids is given as input (--centroid_list). 

