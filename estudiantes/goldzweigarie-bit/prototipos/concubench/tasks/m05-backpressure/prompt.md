# Productor–consumidor con contrapresión

`/workspace/pipeline.py` simula la ingesta de lecturas de sensores urbanos: un
hilo **productor** genera 100 000 paquetes de 4 KB y dos hilos **consumidores**
los procesan (hash iterado, lento). Al final imprime cuántos paquetes procesó y
un XOR de los resultados (no depende del orden).

El productor es mucho más rápido que los consumidores, así que la cola crece
hasta contener casi todos los paquetes (~400 MB). Con el límite de **96 MB** el
proceso muere por OOM.

## Lo que tienes que hacer

Corrige `pipeline.py` para que use memoria acotada **sin perder concurrencia**
(sigue habiendo productor y consumidores en hilos) y sin cambiar el resultado.
No cambies la interfaz:

```
python3 /workspace/pipeline.py <params.json>    # imprime JSON en stdout
{"procesados": 100000, "xor": "0123456789abcdef"}
```

`params.json` trae `seed`, `n`, `size` y `rounds`. No cambies `payload()` ni
`work()`: definen el resultado.

## Cómo se califica

- `params.json` nuevo (semilla aleatoria). Contenedor con 96 MB, 2 CPUs, sin red.
- `procesados` y `xor` exactos.
- OOM, deadlock (más de 120 s) o salida distinta = falla.

## Para probar

```
echo '{"seed": 7, "n": 30000, "size": 4096, "rounds": 20}' > /tmp/p.json
peakmem python3 pipeline.py /tmp/p.json
```
