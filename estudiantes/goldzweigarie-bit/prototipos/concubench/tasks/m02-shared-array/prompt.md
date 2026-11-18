# Procesar un arreglo grande en paralelo sin duplicarlo en memoria

`/workspace/compute.py` lee un arreglo de numpy (`.npy`, 50 millones de
`float64`, **~400 MB**) con lecturas de sensores de calidad del aire. Reparte el
trabajo entre **4 procesos** con `multiprocessing` y calcula:

- `suma_raiz_abs`: la suma de `sqrt(|x|)` sobre todos los elementos
- `mayores_a_2`: cuántos elementos cumplen `x > 2.0`

En producción corre con un límite de **600 MB** de RAM y hoy muere por OOM: el
arreglo se carga completo y luego se copia a cada worker.

## Lo que tienes que hacer

Modifica `compute.py` para que dé el mismo resultado dentro de 600 MB.
**Conserva el paralelismo**: el reporte mide `cpu_s / wall_s`, y una versión
secuencial pasa la prueba de memoria pero se ve en la tabla. No cambies la interfaz:

```
python3 /workspace/compute.py <ruta.npy>      # imprime JSON en stdout
{"suma_raiz_abs": 12345.678, "mayores_a_2": 1234}
```

## Cómo se califica

- Se genera un `.npy` nuevo (semilla aleatoria) y se corre `compute.py` con
  600 MB, 4 CPUs, sin red y `/workspace` en solo lectura.
- `mayores_a_2` debe ser exacto; `suma_raiz_abs` con tolerancia relativa 1e-9.
- La memoria que se cuenta es la **no reclamable** (anónima + memoria
  compartida/tmpfs). La page cache de un archivo mapeado no cuenta, porque el kernel
  la puede liberar. `/dev/shm` sí cuenta.
- Si hay OOM o tarda más de 120 s, falla.

## Para probar

```
python3 gen_sample.py --n 20000000 /tmp/muestra.npy
peakmem python3 compute.py /tmp/muestra.npy
```
