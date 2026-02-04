# Guía para Subir a GitHub

## Pasos para crear el repositorio en GitHub y subirlo:

### 1. Crear una cuenta en GitHub (si no la tienes)
Visita https://github.com/signup

### 2. Crear un nuevo repositorio en GitHub
- Ve a https://github.com/new
- **Repository name**: `TFM-UNIR-2025` (o el nombre que prefieras)
- **Description**: "Sistema de Monitoreo Energético Industrial - Predicción IDE. Aplicación web Flask para predicción de eficiencia energética en instalaciones avícolas usando Machine Learning."
- **Public**: Selecciona esta opción para que sea accesible al público
- **Initialize this repository with**: No selecciones nada (nosotros ya tenemos los archivos)
- Haz clic en "Create repository"

### 3. Configurar Git localmente
Abre PowerShell en la carpeta del proyecto y ejecuta:

```powershell
# Configurar identidad de Git (una sola vez)
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@ejemplo.com"

# Inicializar repositorio local
git init

# Agregar todos los archivos
git add .

# Primer commit
git commit -m "Commit inicial: Sistema de Monitoreo Energético IDE"

# Conectar con el repositorio remoto (reemplaza USERNAME y REPO)
git remote add origin https://github.com/USERNAME/TFM-UNIR-2025.git

# Cambiar rama principal a 'main'
git branch -M main

# Subir al repositorio
git push -u origin main
```

### 4. Verificar que está en línea
- Visita https://github.com/USERNAME/TFM-UNIR-2025
- Deberías ver tu código en el navegador

### 5. Hacer el repositorio público (confirmación)
- En GitHub, ve a Settings > Danger Zone
- Verifica que "Private" NO está activado
- Si está privado, haz clic en "Change to public"

## Nota sobre los archivos del modelo

Si los archivos `.joblib` son muy grandes (>100 MB), GitHub no los permitirá por defecto.
Opciones:
1. Usar Git LFS (Large File Storage)
2. Documentar que deben descargarse por separado
3. Crear una carpeta `Modelo/.gitkeep` como placeholder

Se recomienda crear un archivo `Modelo/README.md` explicando dónde descargar los modelos.
