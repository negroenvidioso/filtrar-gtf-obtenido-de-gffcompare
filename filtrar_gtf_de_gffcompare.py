#!/usr/bin/env python3
import argparse
import sys
import multiprocessing

def procesar_bloque(bloque, codigos_busqueda):
    resultado = []
    anterior = None
    for linea in bloque:
        if linea.startswith('#'):
            resultado.append(linea)
            continue

        elemento = linea.strip().split("\t")
        if len(elemento) < 9:
            continue

        campo = elemento[8]
        subcampos = campo.split("; ")

        try:
            transcript_id = next(s.split()[1].replace('"', '') for s in subcampos
                                 if s.startswith('transcript_id'))
        except StopIteration:
            continue

        if elemento[2] == 'transcript':
            if not codigos_busqueda or any(codigo in linea for codigo in codigos_busqueda):
                resultado.append(linea)
                anterior = transcript_id
        elif elemento[2] == 'exon' and anterior == transcript_id:
            resultado.append(linea)
    return resultado

def procesar_archivo(archivo_entrada, archivo_salida, codigos, num_cores):
    codigos_validos = {'=', 'c', 'j', 'e', 'i', 'o', 'p', 'r', 'u', 'x', 's', 'n', 'y'}
    codigos_filtro = [c.strip() for c in codigos.split(',') if c.strip()]

    for codigo in codigos_filtro:
        if codigo not in codigos_validos:
            print(f"Error: Código de clase '{codigo}' no válido. Códigos válidos: {', '.join(codigos_validos)}", file=sys.stderr)
            sys.exit(1)

    codigos_busqueda = ['class_code "' + codigo + '"' for codigo in codigos_filtro]

    try:
        with open(archivo_entrada, "r") as archivo_original:
            lineas = archivo_original.readlines()

        # Dividir las líneas en bloques para procesamiento paralelo
        bloques = []
        bloque_actual = []
        for linea in lineas:
            if linea.startswith('#'):
                bloques.append([linea])
            else:
                elemento = linea.strip().split("\t")
                if len(elemento) >= 9 and elemento[2] == 'transcript' and bloque_actual:
                    bloques.append(bloque_actual)
                    bloque_actual = []
                bloque_actual.append(linea)
        if bloque_actual:
            bloques.append(bloque_actual)

        # Procesar los bloques en paralelo
        with multiprocessing.Pool(num_cores) as pool:
            resultados = pool.starmap(procesar_bloque, [(bloque, codigos_busqueda) for bloque in bloques])

        # Escribir los resultados en el archivo de salida
        with open(archivo_salida, "w") as nuevo_archivo:
            for resultado in resultados:
                for linea in resultado:
                    nuevo_archivo.write(linea)

    except IOError as e:
        print(f"Error procesando archivos: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
        Filtrador de GTF por códigos de clase de gffcompare

        Filtra un archivo GTF de StringTie conservando solo las transcripciones
        con los códigos de clase especificados y sus exones correspondientes.

        Diseñado por PhD(c) Allan Peñaloza - Otárola
        email allan.penaloza@ug.uchile.cl
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-i', '--input', required=True,
                        help='Archivo GTF de entrada (ej. data.annotated.gtf)')
    parser.add_argument('-o', '--output', required=True,
                        help='Archivo GTF de salida filtrado')
    parser.add_argument('-f', '--filter', default="",
                        help='Códigos de clase para filtrar (ej. u,j,x,=). Si no se especifica, muestra estadísticas.')
    parser.add_argument('-c', '--cores', type=int, default=1,
                        help='Número de núcleos a utilizar (por defecto: 1)')

    args = parser.parse_args()

    if not args.filter:
        print("No se especificaron códigos de filtro. Mostrando códigos disponibles:")
        print("= : Concordancia exacta con referencia")
        print("c : Contenido en referencia")
        print("j : Nueva isoforma potencial")
        print("e : Solapamiento único de exón")
        print("o : Otros solapamientos")
        print("u : Intergénico (transcripción nueva)")
        print("x : Exón en hebra opuesta")
        print("n : (otros códigos disponibles)")
        sys.exit(0)

    procesar_archivo(args.input, args.output, args.filter, args.cores)
