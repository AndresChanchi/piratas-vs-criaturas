# 🏴‍☠️ Piratas vs Criaturas Marinas

Un juego arcade hecho en **Python con Pygame**, donde controlas un barco pirata en una intensa batalla contra criaturas marinas. A medida que el juego avanza, deberás esquivar ataques enemigos, disparar con tus cañones y sobrevivir lo suficiente hasta enfrentarte al **temible jefe final**: un pez de las profundidades con linterna en la cabeza.

---

## 🎮 Cómo jugar

### Movimiento
| Acción         | Tecla(s)              |
|----------------|------------------------|
| Mover arriba   | `W` o `Flecha ↑`       |
| Mover abajo    | `S` o `Flecha ↓`       |
| Mover izquierda| `A` o `Flecha ←`       |
| Mover derecha  | `D` o `Flecha →`       |

### Disparo manual por tipo de cañón
| Cañón                | Tecla de disparo |
|----------------------|------------------|
| Cañones frontales    | `J` o   `SPACE`  |
| Cañones superiores   | `K` o   `V`      |
| Cañones inferiores   | `L` o   `B`      |
| Mortero (especial)   | `I` o   `N`      |

> 💡 Los disparos no son automáticos, debes usar las teclas correspondientes.

### Pausar el juego
Haz clic en el **botón de pausa (arriba a la derecha)** o presiona `ESC`.

---

## ⚙️ Instalación

### 1. Clona el repositorio
```
git clone https://github.com/AndresChanchi/piratas-vs-criaturas.git
```
Abre el proyecto
```
cd piratas-vs-criaturas
````

### 2. Crea un entorno virtual (opcional)

```bash
python -m venv venv
source venv/bin/activate  # En Linux/macOS
venv\Scripts\activate     # En Windows
```

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecuta el juego

```bash
python main.py
```

---

## 📁 Estructura del proyecto

```
piratas-vs-criaturas/
│
├── assets/                     # Imágenes y recursos
│   └── images/
│       └── characters/
│           ├── player/
│           ├── cats/
│           └── enemies/
│
├── collisions.py               # Lógica de colisiones
├── constants.py                # Constantes globales
├── enemy.py                    # Clases de enemigos y jefe
├── main.py                     # Bucle principal del juego
├── menu.py                     # Menú principal y pausa
├── player.py                   # Lógica del jugador
├── weapon.py                   # Cañones y disparos
├── requirements.txt            # Dependencias de Python
└── README.md                   # Este archivo
```

---

## 🎨 Créditos

* Sprites tomados de [itch.io](https://itch.io/) bajo licencias libres para uso no comercial.
* Cañones, efectos y personajes inspirados en juegos como **Cuphead** y títulos retro educativos.
* Música y sonidos no incluidos por defecto.

---

## 🧪 Requisitos técnicos

* Python `>= 3.8`
* Pygame `>= 2.0`

---

## 📝 Notas adicionales

* El juego termina en **Game Over** si la barra de salud llega a cero.
* Puedes reiniciar el juego desde el **menú de pausa** (`ESC` o botón).
* El jefe aparece automáticamente luego de cierto tiempo... si logras sobrevivir lo suficiente. 😉
* Con el botón de puasa puedes reiniciar o ir al home principal del juego


---

¡A disfrutar del caos marino! ⚓🐙🦈


