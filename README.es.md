# Lista de Tareas CLI (Python)

Una aplicación simple de lista de tareas por línea de comandos construida con Python que permite a los usuarios crear, ver, eliminar, guardar y cargar tareas desde un archivo CSV mediante un menú interactivo.

## Características

- Menú interactivo numerado del 1 al 6
- Agregar nuevas tareas
- Ver todas las tareas con posiciones numeradas
- Eliminar tareas por número
- Guardar tareas en un archivo CSV
- Cargar tareas desde un archivo CSV
- Almacenamiento persistente entre ejecuciones
- Servidor web Flask (opcional)

## Tecnologías Utilizadas

- Python 3
- Manejo de archivos (persistencia CSV)
- Menú CLI interactivo
- Interfaz web Flask (opcional)

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/La2ryx/todo-list-cli-ft-AI-Engr-4.git
```

2. Navega al directorio del proyecto:

```bash
cd todo-list-cli-ft-AI-Engr-4
```

3. Ejecuta la aplicación:

```bash
python app.py
```

## Uso

Ejecuta el programa y sigue el menú interactivo:

```
===================================
    LISTA DE TAREAS — MENÚ PRINCIPAL
===================================
  1. Agregar tarea
  2. Listar tareas
  3. Eliminar tarea
  4. Guardar tareas en archivo
  5. Cargar tareas desde archivo
  6. Salir
===================================
```

### Agregar una tarea (opción 1)

```
Título de la tarea: Comprar víveres
Tarea agregada: "Comprar víveres"
```

### Ver todas las tareas (opción 2)

```
Tareas pendientes:
  1. Comprar víveres
  2. Terminar proyecto de Python
  3. Estudiar para el examen
```

### Eliminar una tarea (opción 3)

Muestra las tareas actuales y luego solicita el número de posición a eliminar.

### Guardar / Cargar (opciones 4 y 5)

Persiste la lista en memoria en `todos.csv` o la restaura desde el archivo.

### Servidor Web (opcional)

```bash
python server.py
```

Luego abre `http://localhost:3000` en tu navegador.

## Estructura del Proyecto

```
.
├── app.py          # Aplicación CLI interactiva (5 funciones + menú)
├── test.py         # Pruebas unitarias (17 pruebas)
├── server.py       # Servidor web Flask (opcional)
├── main.py         # Script hello-world mínimo (plantilla inicial)
├── learn.json      # Metadatos del proyecto
├── .gitignore      # Ignora __pycache__ y todos.csv
├── README.md       # Documentación en inglés
└── README.es.md    # Este archivo
```

## Pruebas

Ejecuta el conjunto de pruebas con:

```bash
python test.py
```

Las 17 pruebas deberían pasar, cubriendo:

| Prueba | Cobertura |
|--------|-----------|
| `add_one_task` | Simple, múltiple, caracteres especiales |
| `print_list` | Lista vacía, lista poblada |
| `delete_task` | Primero, medio, último, único, fuera de rango, vacío |
| `save_todos` + `load_todos` | Ida y vuelta, tarea única, vacío, archivo faltante, composición |

## Lo que Aprendí

Durante este proyecto practiqué:

- Funciones de Python operando sobre una lista compartida en memoria
- Patrones de menú CLI interactivo
- Lectura y escritura de archivos CSV
- Pruebas unitarias con `unittest`
- Integración con servidor web
- Desarrollo de aplicaciones de línea de comandos
- Manejo de errores y validación de entrada de usuario
- Flujo de trabajo con Git y GitHub

## Mejoras Futuras

- Estado de completado de tareas
- Prioridades de tareas
- Fechas de vencimiento
- Búsqueda y filtro de tareas
- Salida de terminal con colores
- Mayor cobertura de pruebas

## Autor

**Larry**

GitHub: [https://github.com/La2ryx](https://github.com/La2ryx)
