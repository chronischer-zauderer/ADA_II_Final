import tkinter as tk
from tkinter import ttk, messagebox

from parser import parse_input
from minizinc_generator import generate_mzn

class ConcertModelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador MiniZinc - Segundo Proyecto")
        self.root.geometry("1100x720")
        self.root.minsize(900, 600)

        self._build_ui()

    def _build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # --- Encabezado ---
        header = ttk.Frame(self.root, padding=(16, 14, 16, 8))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        title = ttk.Label(
            header,
            text="Generador de modelo MiniZinc para ubicar el concierto",
            font=("TkDefaultFont", 16, "bold"),
        )
        title.grid(row=0, column=0, sticky="w")

        subtitle = ttk.Label(
            header,
            text="Pegue la entrada con formato N, M y las ciudades. La aplicación generará el código declarativo MiniZinc.",
        )
        subtitle.grid(row=1, column=0, sticky="w", pady=(4, 0))

        # --- Panel Principal (Distribución en Columnas) ---
        main = ttk.Frame(self.root, padding=(16, 8, 16, 16))
        main.grid(row=1, column=0, sticky="nsew")
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(1, weight=1)

        # Sección de Entrada (Izquierda)
        input_frame = ttk.LabelFrame(main, text="Entrada de Datos", padding=12)
        input_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 8))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)

        self.input_text = tk.Text(input_frame, wrap="none", height=22, undo=True)
        self.input_text.grid(row=0, column=0, sticky="nsew")
        input_scroll = ttk.Scrollbar(input_frame, orient="vertical", command=self.input_text.yview)
        input_scroll.grid(row=0, column=1, sticky="ns")
        self.input_text.configure(yscrollcommand=input_scroll.set)

        # Datos de ejemplo por defecto (los del enunciado del proyecto)
        sample_input = """12
5
Palmira 2 3
Cali 10 2
Buga 11 0
Tulua 0 3
Rio Frio 1 2"""
        self.input_text.insert("1.0", sample_input)

        # Controles Centrales / Superiores (Derecha)
        controls = ttk.Frame(main)
        controls.grid(row=0, column=1, sticky="ew", padx=(8, 0), pady=(0, 8))
        controls.columnconfigure(0, weight=1)

        self.generate_button = ttk.Button(
            controls, text="Generar código MiniZinc", command=self.generate_code
        )
        self.generate_button.grid(row=0, column=0, sticky="w")

        self.clear_button = ttk.Button(
            controls, text="Limpiar salida", command=self.clear_output
        )
        self.clear_button.grid(row=0, column=1, sticky="w", padx=(8, 0))

        # Sección de Salida (Derecha Inferior)
        output_frame = ttk.LabelFrame(main, text="Código MiniZinc Declarativo", padding=12)
        output_frame.grid(row=1, column=1, sticky="nsew", padx=(8, 0))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)

        self.output_text = tk.Text(output_frame, wrap="none", height=22, undo=False)
        self.output_text.grid(row=0, column=0, sticky="nsew")
        output_scroll = ttk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        output_scroll.grid(row=0, column=1, sticky="ns")
        self.output_text.configure(yscrollcommand=output_scroll.set)

        self.output_text.insert("1.0", "Aquí aparecerá el modelo MiniZinc generado.")
        self.output_text.configure(state="disabled")

        # --- Barra de Estado (Footer) ---
        status = ttk.Frame(self.root, padding=(16, 0, 16, 14))
        status.grid(row=2, column=0, sticky="ew")
        status.columnconfigure(0, weight=1)

        self.status_var = tk.StringVar(value="Listo para procesar la entrada.")
        status_label = ttk.Label(status, textvariable=self.status_var, font=("TkDefaultFont", 9, "italic"))
        status_label.grid(row=0, column=0, sticky="w")

    def clear_output(self):
        """Limpia el área del editor de salida."""
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", "Aquí aparecerá el modelo MiniZinc generado.")
        self.output_text.configure(state="disabled")
        self.status_var.set("Caja de salida restaurada.")

    def generate_code(self):
        """Manejador del botón que gatilla el pipeline de parsing y compilación a MiniZinc."""
        try:
            raw_text = self.input_text.get("1.0", tk.END)
            size, city_count, cities = parse_input(raw_text)
            code = generate_mzn(size, city_count, cities)
        except ValueError as exc:
            messagebox.showerror("Error en formato de entrada", str(exc))
            self.status_var.set("Error: Revisar los datos de entrada.")
            return

        # Inserción segura en el componente gráfico bloqueado
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", code)
        self.output_text.configure(state="disabled")
        self.status_var.set(f"Modelo MiniZinc compilado exitosamente para M={city_count} ciudades.")
