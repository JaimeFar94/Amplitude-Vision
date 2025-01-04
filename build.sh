#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Inicializar las migraciones si no existen
flask db init || true

# Crear la migración
flask db migrate

# Aplicar la migración
flask db upgrade