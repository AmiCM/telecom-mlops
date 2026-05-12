# 📊 Telecom Employee Churn Prediction: MLOps Framework
Este repositorio contiene un framework integral de MLOps para predecir la rotación de empleados (churn) en una empresa de telecomunicaciones. El proyecto utiliza Databricks Asset Bundles (DABs) para garantizar un ciclo de vida de desarrollo de software (SDLC) robusto, facilitando la transición de experimentos en notebooks a pipelines de producción.

## 🎯 Objetivo del Business Case
La industria de las telecomunicaciones enfrenta una alta competitividad. La pérdida de talento crítico no solo impacta la operación, sino que genera costos de reclutamiento y capacitación equivalentes a 6-9 meses del salario del empleado.

## Propuesta de valor:

Identificación Proactiva: Detectar patrones de abandono antes de que ocurran.

Intervención Basada en Datos: Segmentar empleados en riesgo para aplicar programas de retención personalizados.

Automatización: Reducir la deuda técnica mediante la orquestación automatizada de modelos.

## 🛠️ Stack Tecnológico
Plataforma de Datos: Databricks (Runtime 13.x+).

Orquestación: Databricks Asset Bundles (DABs).

Gobernanza: Unity Catalog (UC).

Tracking: MLflow (Model Registry & Experiment Tracking).

Gestión de Dependencias: uv para una resolución de paquetes ultra rápida.

CI/CD: GitHub Actions.

## 📂 Estructura del Proyecto
El proyecto sigue la estructura estándar de un Asset Bundle, separando la lógica de negocio de la infraestructura:

```
├── databricks.yml          # Configuración principal del bundle (entornos dev/prod)
├── resources/              # Definición de Jobs, Clusters y Pipelines (YAML)
│   ├── churn_job.yml       # Definición del flujo de entrenamiento y evaluación
│   └── inference_job.yml   # Configuración para scoreo por lotes (Batch)
├── src/                    # Código fuente modular
│   ├── training/           # Entrenamiento del modelo y ajuste de hiperparámetros
│   ├── inference/          # Lógica para predicción sobre nuevos datos
│   └── common/             # Funciones de utilidad y transformaciones Spark
├── tests/                  # Pruebas unitarias con pytest
├── pyproject.toml          # Configuración de dependencias con uv
└── README.md
```

## 🚀 Configuración y Despliegue
### 1. Requisitos Previos
- Databricks CLI configurado (databricks configure).
- uv instalado para la gestión de entorno local.

### 2. Instalación Local

1. Clonar el repositorio
```bash
git clone <url-del-repo>
cd <nombre-del-repo>
```

2. Crear entorno virtual e instalar dependencias con uv
```bash
uv sync
```

### 3. Despliegue con Bundles
Para desplegar los recursos (Jobs, Tablas, Modelos) en tu área de desarrollo:

```Bash
# Validar el bundle
databricks bundle validate

# Desplegar en entorno de desarrollo
databricks bundle deploy -t dev
```

## 📈 Ciclo de Vida del Modelo
**Ingesta & Feature Engineering:** Procesamiento de datos de empleados (antigüedad, satisfacción, salario, KPIs de desempeño) mediante Spark SQL.

**Experimentación:** Registro automático de métricas (Accuracy, Recall, F1-Score) en MLflow.

**Gobernanza en Unity Catalog:** Los modelos aprobados se registran en Unity Catalog utilizando alias (@champion / @challenger) para facilitar el despliegue sin cambios de código.

**Monitoreo:** Evaluación continua del sesgo y el drift de los datos de empleados.

## 📊 Métricas de Negocio (KPIs)
**Reducción de Atrición:** Objetivo de disminuir la tasa de rotación en un X% anual.

**ROI de Retención:** Comparativa entre el costo del programa de retención vs. costo de reemplazo de empleados.

**Model Precision:** Minimizar falsos positivos para optimizar el presupuesto de recursos humanos.

## Notas de Implementación
Este proyecto utiliza un enfoque de Infraestructura como Código (IaC). Cualquier cambio en la configuración de los clusters o la frecuencia de los jobs debe realizarse en los archivos dentro de resources/ y desplegarse mediante la CLI de Databricks.