import yaml
import subprocess
import argparse

#Ask for the required arguments
parser=argparse.ArgumentParser(description='Program description')
parser.add_argument('--centroid_list', required='True', help='list of the centroids to compute the trajectories')
args=parser.parse_args()
list_files=args.centroid_list

#Function to read and modify the .yml file
def modificar_variable_yml(ruta_yml, cambios):
    with open(ruta_yml, 'r') as file:
        config = yaml.safe_load(file)

    # Aplicar los cambios
    for path, nuevo_valor in cambios.items():
        keys = path.split('.')
        d = config
        for key in keys[:-1]:
            d = d[key]
        d[keys[-1]] = nuevo_valor

    with open(ruta_yml, 'w') as file:
        yaml.safe_dump(config, file)

#File.yml
yml_file='workflow.yml'

list_with_files=open(list_files, 'rt')
centroid_files=[]
for file in list_with_files:
    centroid_files.append(file[:-1])

# Process every .yml file
k=0
for i in range(len(centroid_files)):
    for j in range(k, len(centroid_files)):
        if centroid_files[i]==centroid_files[j]:
            continue
            
        cambios = {
        'step0_extract_chain.paths.input_structure_path': centroid_files[i],
        'step1_extract_chain.paths.input_structure_path': centroid_files[j]
        }
        modificar_variable_yml(yml_file, cambios)
        # Ejecutar el fichero Python
        resultado = subprocess.run(['python', 'workflow.py', '--config',  yml_file], capture_output=True, text=True)
        print(f"Salida para {centroid_files[j]}:\n", resultado.stdout)
        if resultado.stderr:
            print(f"Errores para {centroid_files[j]}:\n", resultado.stderr)
    k+=1
