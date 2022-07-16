# saturdays_pdf_recognition

### To-do list

- [ ] Recopilación de datos (tesis doctorales).
- [ ] Investigación del estado del arte. Cómo funciona el etiquetado y el entrenamiento de modelos.
- [ ] Entrenamiento de modelos y comparación de rendimientos. 
- [ ] Optimización de hiperparámetros.
- [ ] Medida de rendimiento (accuracy).
- [ ] Testeo con otro tipo de documento.
- [ ] Investigación aprendizaje auto-supervisado. 
- [ ] Deployment (API...).

## How to run the code

First you need to build a virtualenvironment and install the necessary dependencies, as listed in ```requirements.txt```. To do so, you can simply type:

```
source full_setup.sh
```

The file ```main.py``` transforms **pdf** files into images in **png** format. It accepts a directory as an input, in which case it will transform all files within the directory. Use cases:

```
python main.py -n <input_file_name> -p <number_of_pages_to_read (optional)>
```

```
python main.py -i <input_directory> -f <number_of_files_to_read (optional)>
```

The output will be stored inside a new created folder ```images```.