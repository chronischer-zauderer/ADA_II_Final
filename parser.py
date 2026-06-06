def parse_input(raw_text: str):
    """
    Parsea el texto de entrada validando rigurosamente el formato:
    Línea 1: N (Tamaño del Valle)
    Línea 2: M (Cantidad de ciudades)
    Siguientes M líneas: Nombre_Ciudad X Y
    """
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    if len(lines) < 2:
        raise ValueError("La entrada debe tener al menos dos líneas: N y M.")

    try:
        size = int(lines[0])
    except ValueError as exc:
        raise ValueError("La primera línea debe ser un entero N.") from exc

    try:
        city_count = int(lines[1])
    except ValueError as exc:
        raise ValueError("La segunda línea debe ser un entero M.") from exc

    if size <= 0:
        raise ValueError("N (tamaño del mapa) debe ser mayor que cero.")
    if city_count <= 0:
        raise ValueError("M (cantidad de ciudades) debe ser mayor que cero.")
    
    if len(lines) != city_count + 2:
        raise ValueError(
            f"Se esperaban {city_count} líneas de ciudades de acuerdo a M, "
            f"pero se recibieron {len(lines) - 2} líneas de datos."
        )

    cities = []
    for index, line in enumerate(lines[2:], start=1):
        parts = line.split()
        if len(parts) < 3:
            raise ValueError(
                f"La línea {index + 2} debe contener al menos el nombre de la ciudad y las coordenadas X e Y."
            )

        # Maneja correctamente nombres con espacios (ej. "Río Frío")
        name = " ".join(parts[:-2]).strip()
        if not name:
            raise ValueError(f"La línea {index + 2} no contiene un nombre de ciudad válido.")

        try:
            x = int(parts[-2])
            y = int(parts[-1])
        except ValueError as exc:
            raise ValueError(
                f"La línea {index + 2} debe terminar con dos números enteros para las coordenadas X e Y."
            ) from exc

        if not (0 <= x <= size and 0 <= y <= size):
            raise ValueError(
                f"La ciudad '{name}' en la línea {index + 2} tiene coordenadas ({x}, {y}) "
                f"fuera del rango permitido para el mapa (0..{size})."
            )

        cities.append({"name": name, "x": x, "y": y})

    return size, city_count, cities
