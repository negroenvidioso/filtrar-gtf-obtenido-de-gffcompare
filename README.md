# 🧬 Filtrador de GTF por Códigos de Clase de gffcompare

Este script en Python permite filtrar archivos GTF generados por StringTie, conservando únicamente las transcripciones que coinciden con los códigos de clase especificados (según la herramienta `gffcompare`) y sus exones correspondientes.

## 📌 Características

- Filtra transcripciones y exones según códigos de clase (`u`, `j`, `x`, `=`, etc.).
- Soporta procesamiento paralelo utilizando múltiples núcleos.
- Preserva los encabezados y el formato del archivo GTF original.
- Validación de códigos de clase para evitar errores comunes.

## 🛠️ Requisitos

- Python 3.x
- Sistema operativo compatible con `multiprocessing` (Linux, macOS, Windows)

## 🚀 Uso

```bash
python3 filtrador_gtf.py -i archivo_entrada.gtf -o archivo_salida.gtf -f u,j,x -c 4
```

### Argumentos

| Opción | Descripción |
|--------|-------------|
| `-i`, `--input` | Ruta al archivo GTF de entrada |
| `-o`, `--output` | Ruta al archivo GTF de salida filtrado |
| `-f`, `--filter` | Códigos de clase a filtrar (ej. `u,j,x,=`). Si se omite, se muestran los códigos disponibles |
| `-c`, `--cores` | Número de núcleos a utilizar para procesamiento paralelo (por defecto: 1) |

## 🧪 Ejemplo

```bash
python3 filtrador_gtf.py -i data.annotated.gtf -o data.filtrado.gtf -f u,j -c 2
```

Este comando filtrará las transcripciones con códigos `u` y `j`, utilizando 2 núcleos de CPU.

## 📖 Códigos de Clase Comunes

- `=` : Concordancia exacta con la referencia
- `c` : Contenido en referencia
- `j` : Nueva isoforma potencial
- `e` : Solapamiento único de exón
- `o` : Otros solapamientos
- `u` : Intergénico (transcripción nueva)
- `x` : Exón en hebra opuesta
- `n`, `s`, `p`, `r`, `i`, `y` : Otros códigos posibles

## 👨‍🔬 Autor

**Allan Peñaloza - Otárola, PhD(c)**  
📧 allan.penaloza@ug.uchile.cl
