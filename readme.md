# Helm Chart Manager

Una aplicación en Python para descubrir y gestionar Helm charts mediante Artifact Hub. Esta herramienta permite buscar, instalar y gestionar charts de Helm en clusters de Kubernetes.

## Requisitos Previos

- Python 3.7+
- Helm instalado ([Guía de instalación de Helm](https://helm.sh/docs/intro/install/))
- Cluster de Kubernetes (Minikube o Kind)
- pip (gestor de paquetes de Python)

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/alexrubenmartinez/manageHelmCharts
cd helm-chart-manager
```

2. Crear un entorno virtual:

```bash
# Linux/macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Configuración del Cluster

### Con Minikube

1. Instalar Minikube:

```bash
# Linux/macOS
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Windows (con chocolatey)
choco install minikube
```

2. Iniciar el cluster:

```bash
minikube start
```

3. Verificar la instalación:

```bash
minikube status
kubectl get nodes
```

## Uso

La aplicación proporciona varios comandos para gestionar charts de Helm:

### Buscar Charts

Buscar charts disponibles en Artifact Hub:

```bash
python manage_helm_charts.py search redis
```

### Ver Detalles de un Chart

Obtener información detallada sobre un chart específico:

```bash
python manage_helm_charts.py info bitnami/redis
```

### Instalar un Chart

Instalar un chart en el cluster:

```bash
python manage_helm_charts.py install bitnami/redis --release-name mi-redis --namespace default
```

Opciones disponibles:

- `--release-name`: Nombre para la instalación (requerido)
- `--namespace`: Namespace de Kubernetes (por defecto: "default")
- `--version`: Versión específica del chart a instalar

### Listar Releases Instalados

Ver todos los releases de Helm instalados:

```bash
python manage_helm_charts.py list-releases
```

Filtrar por namespace:

```bash
python manage_helm_charts.py list-releases --namespace mi-namespace
```

### Desinstalar un Release

Eliminar un release instalado:

```bash
python manage_helm_charts.py uninstall mi-redis
```

## Verificación y Monitoreo

### Verificar la Instalación

1. Ver los pods creados:

```bash
kubectl get pods
```

2. Ver los servicios:

```bash
kubectl get services
```

3. Ver detalles de un pod:

```bash
kubectl describe pod nombre-del-pod
```

### Dashboard de Minikube

Para una visualización gráfica del cluster:

```bash
minikube dashboard
```

## Solución de Problemas

### Problemas Comunes

1. **Pods no visibles**:

```bash
# Verificar todos los namespaces
kubectl get pods --all-namespaces
```

2. **Problemas con los Pods**:

```bash
# Ver logs del pod
kubectl logs nombre-del-pod

# Ver eventos del pod
kubectl describe pod nombre-del-pod
```

3. **Problemas con Helm**:

```bash
# Actualizar repositorios
helm repo update

# Ver repositorios configurados
helm repo list
```

### Reiniciar el Entorno

Si necesitas empezar desde cero:

```bash
minikube delete
minikube start
```

## Referencias

- [Documentación de Helm](https://helm.sh/docs/)
- [Documentación de Minikube](https://minikube.sigs.k8s.io/docs/)
- [Artifact Hub](https://artifacthub.io/)
- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
