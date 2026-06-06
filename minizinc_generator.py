def generate_mzn(size: int, city_count: int, cities):
    """
    Genera el código formateado para MiniZinc utilizando un enfoque de optimización
    Minimax balanceado (minimizar la distancia máxima y reducir la distancia total).
    """
    xs = ", ".join(str(city["x"]) for city in cities)
    ys = ", ".join(str(city["y"]) for city in cities)
    names = ", ".join(f'"{city["name"]}"' for city in cities)

    return f"""% =================================================================
% Modelo MiniZinc generado automáticamente para la ubicación del concierto
% Curso: Análisis y Diseño de Algoritmos - Proyecto de Optimización
% =================================================================

int: N = {size}; % Dimensión del Valle del Cauca (Cuadrado de N x N)
int: M = {city_count}; % Cantidad de ciudades evaluadas

% Vectores constantes con la información de las ciudades
array[1..M] of int: city_x = [{xs}];
array[1..M] of int: city_y = [{ys}];
array[1..M] of string: city_name = [{names}];

% --- Variables de Decisión ---
var 0..N: x; % Coordenada X del concierto
var 0..N: y; % Coordenada Y del concierto

% Vector de distancias de decisión del solucionador
array[1..M] of var 0..2 * N: dist;

% --- Restricciones ---

% 1. Definición matemática de la Distancia Manhattan para cada ciudad
constraint forall(i in 1..M)(
    dist[i] = abs(x - city_x[i]) + abs(y - city_y[i])
);

% 2. Restricción de Exclusión: El concierto NO puede estar en la misma coordenada que una ciudad
constraint forall(i in 1..M)(
    (x != city_x[i]) \\/ (y != city_y[i])
);

% --- Variables de Análisis Teórico y del Entorno ---
var int: d_max = max(dist);
var int: d_min = min(dist);
var int: total_dist = sum(dist);
var int: spread = d_max - d_min;

% --- Función Objetivo (Criterio de Equidad de Ingeniería) ---
% Se prioriza minimizar la distancia máxima (criterio minimax)
% y luego la distancia total como desempate.
solve minimize (d_max * 100) + total_dist;

% --- Salida de Resultados ---
output [
  "Solución encontrada para el concierto:\\n",
  "Coordenada X = ", show(x), "\\n",
  "Coordenada Y = ", show(y), "\\n\\n",

  "=== Métricas de Optimización ===\\n",
  "Distancia máxima (peor caso): ", show(d_max), " km\\n",
  "Distancia mínima (mejor caso): ", show(d_min), " km\\n",
  "Dispersión (Spread): ", show(spread), " km\\n",
  "Suma total de trayectos: ", show(total_dist), " km\\n\\n",

  "=== Distancias por ciudad ===\\n"
]
++
[
  city_name[i] ++ " -> " ++ show(dist[i]) ++ " km\\n"
  | i in 1..M
];
"""