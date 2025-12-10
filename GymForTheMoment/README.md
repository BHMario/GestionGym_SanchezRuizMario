# 🏋️‍♂️ Gym For The Moment

Aplicación de escritorio desarrollada en **Python** con **Tkinter** para la gestión integral de un gimnasio. Permite el registro y autenticación de clientes, reserva de aparatos y clases en franjas de 30 minutos, generación de recibos mensuales y control de clientes morosos.

---


## Requisitos

- Python 3.8+
- SQLite (integrado en Python)

---

## Instalación rápida

```powershell
git clone AQUI_PONER_URL_DEL_REPOSITORIO
cd GymForTheMoment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Ejecución

```powershell
python main.py
```

La GUI se inicia en modo gráfico y presenta el formulario de login. Desde el menú se accede a registro, reservas, pagos y reportes.

---

## Usuarios de prueba

Para probar la aplicación sin registrarse, puedes usar los siguientes usuarios predefinidos:

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| `admin` | `admin123` | Administrador |
| `cliente1` | `pass123` | Cliente |
| `Mario` | `123` | Cliente |

También puedes registrar nuevos usuarios directamente desde la interfaz de login seleccionando la opción "Registrarse".

---

## Requisitos funcionales

- Registro y login de clientes
- Reserva de aparatos (franjas de 30 minutos)
- Reserva y gestión de clases
- Generación de recibos mensuales
- Listado de morosos y consultas de pago

---

## Diagramas

Los diagramas están disponibles en la carpeta `docs/`:

- [Diagrama de Casos de Uso](docs/diagrama_casos_uso.png)
- [Diagrama ER](docs/diagrama_er.png)

---

## Modelo de datos (DDL)

El esquema abajo es un DDL resumido que refleja las entidades principales del sistema. Se puede ejecutar tal cual en SQLite para crear la base mínima.

```sql
-- Tabla CLIENTE
CREATE TABLE CLIENTE (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    contrasena TEXT NOT NULL,
    nombre_completo TEXT NOT NULL,
    telefono TEXT,
    estado TEXT DEFAULT 'activo',
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla APARATO
CREATE TABLE APARATO (
    id_aparato INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    tipo TEXT NOT NULL,
    estado TEXT DEFAULT 'activo',
    capacidad_simultanea INTEGER DEFAULT 1
);

-- Tabla CLASE
CREATE TABLE CLASE (
    id_clase INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    instructor TEXT NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    dias_semana TEXT NOT NULL,
    capacidad INTEGER NOT NULL,
    estado TEXT DEFAULT 'activa'
);

-- Tabla RESERVA
CREATE TABLE RESERVA (
    id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    id_aparato INTEGER,
    id_clase INTEGER,
    fecha_inicio DATETIME NOT NULL,
    fecha_fin DATETIME NOT NULL,
    estado TEXT DEFAULT 'activa',
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id_cliente) ON DELETE CASCADE,
    FOREIGN KEY (id_aparato) REFERENCES APARATO(id_aparato) ON DELETE SET NULL,
    FOREIGN KEY (id_clase) REFERENCES CLASE(id_clase) ON DELETE SET NULL
);

-- Tabla RECIBO
CREATE TABLE RECIBO (
    id_recibo INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    numero_recibo TEXT UNIQUE NOT NULL,
    monto REAL DEFAULT 50.00,
    mes_facturado TEXT NOT NULL,
    estado TEXT DEFAULT 'pendiente',
    fecha_emision DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_vencimiento DATE NOT NULL,
    fecha_pago DATE,
    metodo_pago TEXT,
    FOREIGN KEY (id_cliente) REFERENCES CLIENTE(id_cliente) ON DELETE CASCADE
);
```

---

## Estructura (Resumida) del proyecto

```
GymForTheMoment/
├── README.md
├── main.py
├── gimnasio.db
├── diagramas/               # Diagramas (Casos de Uso, ER, Arquitectura)
├── interfaz/                # Interfaz gráfica (Tkinter)
├── servicios/               # Lógica de negocio
├── modelos/                 # Entidades del dominio
└── utilidades/              # Validadores y utilidades
```

---

## Autor

Mario Sánchez Ruiz

- GitHub: [@BHMario](https://github.com/BHMario)
- Email: mariosanrui1612@gmail.com
