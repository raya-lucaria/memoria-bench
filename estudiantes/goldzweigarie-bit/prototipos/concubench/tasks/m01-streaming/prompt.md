# Agregar viajes por alcaldía sin quedarse sin memoria

En `/workspace/agg.py` hay un script que lee un CSV de viajes en la CDMX y
calcula, por alcaldía, el número de viajes, la tarifa total y la distancia
media. Funciona con archivos pequeños, pero en producción el archivo tiene unos
**5 millones de filas (~200 MB)** y el proceso corre con un límite de
**96 MB de RAM**: hoy lo mata el OOM killer.

## Lo que tienes que hacer

Modifica `agg.py` para que produzca **exactamente la misma salida** usando poca
memoria. No cambies la interfaz:

```
python3 /workspace/agg.py <ruta_al_csv>    # imprime JSON en stdout
```

## Formato

Entrada (con encabezado): `trip_id,alcaldia,distance_km,duration_min,fare_mxn`

Salida: un objeto JSON con una entrada por alcaldía presente en el archivo:

```json
{"Coyoacán": {"viajes": 123, "tarifa_total": 4567.89, "distancia_media_km": 4.1234}, ...}
```

## Cómo se califica

- Se genera un CSV nuevo (semilla aleatoria) y se corre tu `agg.py` en un
  contenedor con 96 MB, 1 CPU, sin red y con `/workspace` en solo lectura.
- `viajes` debe ser exacto; `tarifa_total` y `distancia_media_km` con
  tolerancia relativa de 1e-6.
- Si el proceso muere por OOM o tarda más de 120 s, falla.

## Para probar

```
python3 gen_sample.py --rows 300000 /tmp/muestra.csv
peakmem python3 agg.py /tmp/muestra.csv > /tmp/salida.json
```

`peakmem` reporta el pico de memoria. Con 300 000 filas, el pico debería mantenerse
casi igual cuando subes a 3 000 000.
