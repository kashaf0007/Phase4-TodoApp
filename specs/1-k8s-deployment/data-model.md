# Data Model: Kubernetes Deployment Resources

**Feature**: 1-k8s-deployment | **Date**: 2026-01-29

## Kubernetes Resource Models

### Deployment
**Description**: Defines desired state for application pods with replica management
**Fields**:
- `apiVersion`: Kubernetes API version (apps/v1)
- `kind`: Resource type (Deployment)
- `metadata.name`: Unique identifier for the deployment
- `metadata.namespace`: Namespace for resource isolation
- `spec.replicas`: Desired number of pod replicas
- `spec.selector.matchLabels`: Label selector for pods
- `spec.template.metadata.labels`: Labels applied to pods
- `spec.template.spec.containers`: Container definitions
- `spec.template.spec.containers[].name`: Container name
- `spec.template.spec.containers[].image`: Container image reference
- `spec.template.spec.containers[].ports`: Container port mappings
- `spec.template.spec.containers[].resources`: Resource requests and limits
- `spec.template.spec.containers[].livenessProbe`: Liveness probe configuration
- `spec.template.spec.containers[].readinessProbe`: Readiness probe configuration

**Validation Rules**:
- `replicas` must be >= 1 for availability
- `image` must reference a valid container registry
- `resources.requests` must be <= `resources.limits`

### Service
**Description**: Provides stable network endpoint for applications within the cluster
**Fields**:
- `apiVersion`: Kubernetes API version (v1)
- `kind`: Resource type (Service)
- `metadata.name`: Unique identifier for the service
- `metadata.namespace`: Namespace for resource isolation
- `spec.selector`: Selector for pods to expose
- `spec.ports`: Port mappings
- `spec.type`: Service type (ClusterIP, NodePort, LoadBalancer)
- `spec.clusterIP`: Internal cluster IP (if specified)

**Validation Rules**:
- `selector` must match labels on target pods
- `ports[].port` must be valid port numbers (1-65535)
- `type` must be one of ClusterIP, NodePort, LoadBalancer

### PersistentVolumeClaim
**Description**: Requests storage resources for persistent data storage
**Fields**:
- `apiVersion`: Kubernetes API version (v1)
- `kind`: Resource type (PersistentVolumeClaim)
- `metadata.name`: Unique identifier for the PVC
- `metadata.namespace`: Namespace for resource isolation
- `spec.accessModes`: Access modes (ReadWriteOnce, ReadOnlyMany, etc.)
- `spec.resources.requests.storage`: Storage capacity request
- `spec.storageClassName`: Storage class name (optional)

**Validation Rules**:
- `spec.resources.requests.storage` must be >= 1Gi for database
- `spec.accessModes` must include ReadWriteOnce for database
- `spec.storageClassName` must reference existing storage class if specified

### StatefulSet
**Description**: Manages stateful applications with persistent storage and ordered deployment
**Fields**:
- `apiVersion`: Kubernetes API version (apps/v1)
- `kind`: Resource type (StatefulSet)
- `metadata.name`: Unique identifier for the StatefulSet
- `metadata.namespace`: Namespace for resource isolation
- `spec.replicas`: Desired number of pod replicas
- `spec.selector.matchLabels`: Label selector for pods
- `spec.template.metadata.labels`: Labels applied to pods
- `spec.template.spec.containers`: Container definitions
- `spec.volumeClaimTemplates`: Templates for persistent volume claims

**Validation Rules**:
- `replicas` should be 1 for database to ensure data consistency
- `volumeClaimTemplates` must be defined for persistent storage

### ConfigMap
**Description**: Stores non-sensitive configuration data for applications
**Fields**:
- `apiVersion`: Kubernetes API version (v1)
- `kind`: Resource type (ConfigMap)
- `metadata.name`: Unique identifier for the ConfigMap
- `metadata.namespace`: Namespace for resource isolation
- `data`: Key-value pairs of configuration data

**Validation Rules**:
- `data` keys must be valid DNS labels
- `data` values must be strings

### Secret
**Description**: Stores sensitive information like passwords and tokens securely
**Fields**:
- `apiVersion`: Kubernetes API version (v1)
- `kind`: Resource type (Secret)
- `metadata.name`: Unique identifier for the Secret
- `metadata.namespace`: Namespace for resource isolation
- `type`: Secret type (Opaque, kubernetes.io/basic-auth, etc.)
- `data`: Base64-encoded key-value pairs of sensitive data
- `stringData`: Plaintext key-value pairs (encoded automatically)

**Validation Rules**:
- `data` values must be base64 encoded
- `stringData` values are automatically converted to base64
- `type` must be a valid secret type

### Ingress
**Description**: Manages external access to services via HTTP routes
**Fields**:
- `apiVersion`: Kubernetes API version (networking.k8s.io/v1)
- `kind`: Resource type (Ingress)
- `metadata.name`: Unique identifier for the Ingress
- `metadata.namespace`: Namespace for resource isolation
- `spec.rules`: List of host/path rules
- `spec.rules[].host`: Hostname for the rule
- `spec.rules[].http.paths`: Path-based routing rules
- `spec.rules[].http.paths[].path`: Path pattern
- `spec.rules[].http.paths[].pathType`: Path matching type (Prefix, Exact, ImplementationSpecific)
- `spec.rules[].http.paths[].backend.service.name`: Backend service name
- `spec.rules[].http.paths[].backend.service.port.number`: Backend service port

**Validation Rules**:
- `spec.rules[].http.paths[].path` must be valid path patterns
- `spec.rules[].http.paths[].backend.service.name` must reference existing services
- `spec.rules[].http.paths[].backend.service.port.number` must reference valid service ports