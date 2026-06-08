def generate_mzn(size: int, city_count: int, cities):
    """
    Genera el código MiniZinc para ubicar el concierto utilizando:
    1. Criterio minimax (minimizar la peor distancia).
    2. Minimizar la dispersión entre ciudades (spread).
    3. Minimizar la distancia total como desempate.
    """

    xs = ", ".join(str(city["x"]) for city in cities)
    ys = ", ".join(str(city["y"]) for city in cities)
    names = ", ".join(f'"{city["name"]}"' for city in cities)

    return f"""% =================================================================
% Modelo MiniZinc generado automáticamente para la ubicación del concierto
% Criterio de Equidad Mejorado
% =================================================================

int: N = {size}; % Dimensión del mapa (0..N)
int: M = {city_count}; % Cantidad de ciudades

% Información de las ciudades
array[1..M] of int: city_x = [{xs}];
array[1..M] of int: city_y = [{ys}];
array[1..M] of string: city_name = [{names}];

% --- Variables de Decisión ---
var 0..N: x;
var 0..N: y;

% Distancias Manhattan desde el concierto a cada ciudad
array[1..M] of var 0..2 * N: dist;

% --- Restricciones ---

% Distancia Manhattan
constraint forall(i in 1..M)(
    dist[i] = abs(x - city_x[i]) + abs(y - city_y[i])
);

% El concierto no puede ubicarse exactamente sobre una ciudad
constraint forall(i in 1..M)(
    (x != city_x[i]) \\/ (y != city_y[i])
);

% --- Métricas de análisis ---
var int: d_max = max(dist);
var int: d_min = min(dist);
var int: total_dist = sum(dist);
var int: spread = d_max - d_min;

% --- Función Objetivo ---
%
% Prioridad:
% 1. Minimizar la peor distancia (criterio minimax)
% 2. Minimizar la dispersión entre ciudades
% 3. Minimizar la distancia total
%
solve minimize
    (d_max * 10000)
  + (spread * 100)
  + total_dist;

% --- Salida ---
output [
  "==============================\\n",
  "UBICACIÓN ÓPTIMA DEL CONCIERTO\\n",
  "==============================\\n\\n",

  "Coordenada X: ", show(x), "\\n",
  "Coordenada Y: ", show(y), "\\n\\n",

  "=== Métricas de Equidad ===\\n",
  "Distancia máxima: ", show(d_max), " km\\n",
  "Distancia mínima: ", show(d_min), " km\\n",
  "Spread: ", show(spread), " km\\n",
  "Distancia total: ", show(total_dist), " km\\n\\n",

  "=== Distancias por ciudad ===\\n"
]
++
[
  city_name[i] ++ ": " ++ show(dist[i]) ++ " km\\n"
  | i in 1..M
];
"""
