import matplotlib.pyplot as plt

cities = [
    ("A", 1, 1),
    ("B", 2, 2),
    ("C", 3, 3),
    ("D", 4, 4),
    ("E", 5, 5),
    ("F", 6, 6),
    ("G", 7, 7),
    ("H", 8, 8),
    ("I", 9, 9),
    ("J", 10, 10),
    ("K", 90, 90),
    ("L", 91, 91),
    ("M", 92, 92),
    ("N", 93, 93),
    ("O", 94, 94),
    ("P", 95, 95),
    ("Q", 96, 96),
    ("R", 97, 97),
    ("S", 98, 98),
    ("T", 99, 99)
]

concert_x = 90
concert_y = 10
N = 100

plt.figure(figsize=(8, 8))

# Ciudades
for name, x, y in cities:
    plt.scatter(x, y, s=150)
    plt.text(x + 0.15, y + 0.15, name)

# Concierto
plt.scatter(
    concert_x,
    concert_y,
    marker="*",
    s=400
)

plt.text(
    concert_x + 0.15,
    concert_y + 0.15,
    "Concierto"
)

plt.xlim(-0.5, N + 0.5)
plt.ylim(-0.5, N + 0.5)

plt.xticks(range(N + 1))
plt.yticks(range(N + 1))

plt.grid(True)

plt.title("Ubicación Óptima del Concierto")

plt.savefig("solucion_optima.png", bbox_inches="tight")

plt.show()