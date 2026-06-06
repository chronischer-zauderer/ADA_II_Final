# ADA_II_Final

Aplicacion de escritorio en Python para generar el modelo MiniZinc del segundo proyecto de Optimizacion.

## Ejecucion

```bash
python3 app.py
```

## Funcionamiento

La interfaz permite pegar la entrada con el formato solicitado:

1. N, el tamano del cuadrado.
2. M, el numero de ciudades.
3. M lineas con nombre de ciudad y coordenadas X Y.

Al presionar el boton de generacion, la aplicacion valida la entrada y construye un archivo MiniZinc que modela la ubicacion del concierto sin coincidir con ninguna ciudad y minimizando la dispersion de las distancias Manhattan entre el punto elegido y las ciudades.