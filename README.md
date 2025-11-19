# CRM App

Aplicación CRM desarrollada en Django para gestionar Representantes, Compañías, Clientes e Interacciones.

## Requisitos Previos

- Python 3.10 o superior (Probado con 3.14)

## Guía de Instalación y Ejecución

Siga estos pasos para configurar y ejecutar el proyecto en su entorno local.

### 1. Configurar el Entorno Virtual

Es recomendable utilizar un entorno virtual para aislar las dependencias del proyecto.

> **Nota:** Asegúrese de abrir su terminal en la carpeta raíz del proyecto antes de ejecutar los siguientes comandos.

**En Windows (PowerShell):**
```powershell
# Crear el entorno virtual
python -m venv .venv

# Activar el entorno virtual
.\.venv\Scripts\Activate.ps1
```

**En macOS/Linux:**
```bash
# Crear el entorno virtual
python3 -m venv .venv

# Activar el entorno virtual
source .venv/bin/activate
```

### 2. Instalar Dependencias

Una vez activado el entorno virtual, instale las librerías necesarias:

```bash
pip install -r requirements.txt
```

### 3. Configurar la Base de Datos

Ejecute las migraciones para crear las tablas en la base de datos (SQLite por defecto):

```bash
python manage.py migrate
```

### 4. Poblar Datos de Prueba (Seed)

El proyecto incluye un comando para generar los datos ficticios requeridos (3 representantes, 1000 clientes, ~500 interacciones por cliente):

```bash
python manage.py seed_demo
```
*Nota: Este proceso puede tardar unos minutos debido a la cantidad de datos (aprox. 500,000 registros de interacciones).*

### 5. Ejecutar el Servidor

Inicie el servidor de desarrollo:

```bash
python manage.py runserver
```

### 6. Acceder a la Vista Principal

Abra su navegador web e ingrese a la siguiente dirección:

👉 **http://127.0.0.1:8000/**

Aquí verá la lista de clientes con sus detalles, últimas interacciones y opciones de filtrado.

---

## Credenciales de Prueba

El comando `seed_demo` crea los siguientes usuarios representantes con acceso al panel de administración (`/admin`):

- **Usuarios:** `rep1`, `rep2`, `rep3`
- **Contraseña:** `password123`
