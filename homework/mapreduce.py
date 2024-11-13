"""Map/Reduce immplementation"""

# pylint: disable=broad-exception-raised

import fileinput
import glob
import os.path


#carga los archivos 
def _load_input(input_directory):
    sequence = []
    files = glob.glob(f"{input_directory}/*")   #abre todos los archivos del input_directory
    with fileinput.input(files=files) as f:
        for line in f:
            sequence.append((fileinput.filename(), line))   #lee cada linea de cada archivo y la guarda en un arreglo como nombreArchivo: contenidoLinea (Y lo hace repetidamente linea por linea)
    return sequence


#ordena las tuplas de la lista
def _shuffle_and_sort(sequence):
    return sorted(sequence, key=lambda x: x[0])   #ordena por el primer elemento de la tupla osea el nombre del archivo
  
  
def _create_ouptput_directory(output_directory):
    if os.path.exists(output_directory):
        for file in glob.glob(f"{output_directory}/*"):
            os.remove(file)
        os.rmdir(output_directory)
    os.makedirs(output_directory)


def _save_output(output_directory, sequence):
    with open(f"{output_directory}/part-00000", "w", encoding="utf-8") as f:
        for key, value in sequence:
            f.write(f"{key}\t{value}\n")


def _create_marker(output_directory):
    """Create Marker"""
    with open(f"{output_directory}/_SUCCESS", "w", encoding="utf-8") as f:
        f.write("")


def run_mapreduce_job(mapper, reducer, input_directory, output_directory):
    """Job"""
    sequence = _load_input(input_directory)
    sequence = mapper(sequence)
    sequence = _shuffle_and_sort(sequence)
    sequence = reducer(sequence)
    _create_ouptput_directory(output_directory)
    _save_output(output_directory, sequence)
    _create_marker(output_directory)