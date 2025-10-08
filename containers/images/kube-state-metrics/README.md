Of course. Running `kube-state-metrics` via a simple `docker run` command is misleading, as it requires access to the Kubernetes API server to function correctly. The primary and intended use is deployment within a Kubernetes cluster.

Here is the revised `README.md` with the `docker run` examples removed and the focus shifted to in-cluster deployment.

-----

# kube-state-metrics packaged by SourceMation

kube-state-metrics (KSM) is a simple service that listens to the Kubernetes API server and generates metrics about the state of Kubernetes objects. It provides valuable insights into cluster health by exposing metrics for deployments, nodes, pods, and other Kubernetes resources without modifying the objects themselves.

This kube-state-metrics distribution is provided by the SourceMation packaging team, built on a secure Debian 12 Slim base image with kube-state-metrics.

## Deployment

`kube-state-metrics` is designed to be deployed within a Kubernetes cluster. Below are common deployment patterns.

### Standard Deployment

This example deploys `kube-state-metrics` as a single-replica Deployment. This is suitable for most small to medium-sized clusters.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: kube-state-metrics
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: kube-state-metrics
rules:
- apiGroups: [""]
  resources:
  - configmaps
  - secrets
  - nodes
  - pods
  - services
  - resourcequotas
  - replicationcontrollers
  - limitranges
  - persistentvolumeclaims
  - persistentvolumes
  - namespaces
  - endpoints
  verbs: ["list", "watch"]
- apiGroups: ["apps"]
  resources:
  - statefulsets
  - daemonsets
  - deployments
  - replicasets
  verbs: ["list", "watch"]
- apiGroups: ["batch"]
  resources:
  - cronjobs
  - jobs
  verbs: ["list", "watch"]
- apiGroups: ["autoscaling"]
  resources:
  - horizontalpodautoscalers
  verbs: ["list", "watch"]
- apiGroups: ["policy"]
  resources:
  - poddisruptionbudgets
  verbs: ["list", "watch"]
- apiGroups: ["certificates.k8s.io"]
  resources:
  - certificatesigningrequests
  verbs: ["list", "watch"]
- apiGroups: ["storage.k8s.io"]
  resources:
  - storageclasses
  - volumeattachments
  verbs: ["list", "watch"]
- apiGroups: ["admissionregistration.k8s.io"]
  resources:
  - mutatingwebhookconfigurations
  - validatingwebhookconfigurations
  verbs: ["list", "watch"]
- apiGroups: ["networking.k8s.io"]
  resources:
  - networkpolicies
  - ingresses
  verbs: ["list", "watch"]
- apiGroups: ["coordination.k8s.io"]
  resources:
  - leases
  verbs: ["list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: kube-state-metrics
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: kube-state-metrics
subjects:
- kind: ServiceAccount
  name: kube-state-metrics
  namespace: kube-system
---
apiVersion: v1
kind: Service
metadata:
  name: kube-state-metrics
  namespace: kube-system
  labels:
    app.kubernetes.io/name: kube-state-metrics
    app.kubernetes.io/version: v2.17.0
spec:
  clusterIP: None
  ports:
  - name: http-metrics
    port: 8080
    targetPort: http-metrics
    protocol: TCP
  - name: telemetry
    port: 8081
    targetPort: telemetry
    protocol: TCP
  selector:
    app.kubernetes.io/name: kube-state-metrics
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kube-state-metrics
  namespace: kube-system
  labels:
    app.kubernetes.io/name: kube-state-metrics
    app.kubernetes.io/version: v2.17.0
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: kube-state-metrics
  template:
    metadata:
      labels:
        app.kubernetes.io/name: kube-state-metrics
        app.kubernetes.io/version: v2.17.0
    spec:
      serviceAccountName: kube-state-metrics
      containers:
      - name: kube-state-metrics
        image: sourcemation/kube-state-metrics:latest
        ports:
        - name: http-metrics
          containerPort: 8080
        - name: telemetry
          containerPort: 8081
        livenessProbe:
          httpGet:
            path: /livez
            port: 8080
          initialDelaySeconds: 5
          timeoutSeconds: 5
        readinessProbe:
          httpGet:
            path: /readyz
            port: 8081
          initialDelaySeconds: 5
          timeoutSeconds: 5
        resources:
          requests:
            cpu: 100m
            memory: 250Mi
          limits:
            cpu: 200m
            memory: 500Mi
```

### Sharded Deployment with StatefulSet

For large clusters, you can deploy `kube-state-metrics` with automatic sharding using a StatefulSet to horizontally scale and distribute the load.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: kube-state-metrics
  namespace: kube-system
  labels:
    app.kubernetes.io/name: kube-state-metrics
spec:
  clusterIP: None
  ports:
  - name: http-metrics
    port: 8080
    targetPort: http-metrics
  - name: telemetry
    port: 8081
    targetPort: telemetry
  selector:
    app.kubernetes.io/name: kube-state-metrics
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: kube-state-metrics
  namespace: kube-system
spec:
  serviceName: "kube-state-metrics"
  replicas: 3
  selector:
    matchLabels:
      app.kubernetes.io/name: kube-state-metrics
  template:
    metadata:
      labels:
        app.kubernetes.io/name: kube-state-metrics
    spec:
      serviceAccountName: kube-state-metrics
      containers:
      - name: kube-state-metrics
        image: sourcemation/kube-state-metrics:latest
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        args:
        - --pod=$(POD_NAME)
        - --pod-namespace=$(POD_NAMESPACE)
        ports:
        - name: http-metrics
          containerPort: 8080
        - name: telemetry
          containerPort: 8081
        resources:
          requests:
            cpu: 100m
            memory: 150Mi
          limits:
            cpu: 200m
            memory: 300Mi
```

### DaemonSet Deployment for Pod Metrics

Deploy as a DaemonSet to collect node-specific pod metrics. This pattern is useful for getting detailed metrics on a per-node basis.

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: kube-state-metrics
  namespace: kube-system
  labels:
    app.kubernetes.io/name: kube-state-metrics
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: kube-state-metrics
  template:
    metadata:
      labels:
        app.kubernetes.io/name: kube-state-metrics
    spec:
      serviceAccountName: kube-state-metrics
      containers:
      - name: kube-state-metrics
        image: sourcemation/kube-state-metrics:latest
        env:
        - name: NODE_NAME
          valueFrom:
            fieldRef:
              fieldPath: spec.nodeName
        args:
        - --resource=pods
        - --node=$(NODE_NAME)
        ports:
        - name: http-metrics
          containerPort: 8080
        - name: telemetry
          containerPort: 8081
        resources:
          requests:
            cpu: 50m
            memory: 100Mi
          limits:
            cpu: 100m
            memory: 200Mi
---
# Deployment for unscheduled pods
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kube-state-metrics-unscheduled
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: kube-state-metrics-unscheduled
  template:
    metadata:
      labels:
        app.kubernetes.io/name: kube-state-metrics-unscheduled
    spec:
      serviceAccountName: kube-state-metrics
      containers:
      - name: kube-state-metrics
        image: sourcemation/kube-state-metrics:latest
        args:
        - --resources=pods
        - --track-unscheduled-pods
        ports:
        - name: http-metrics
          containerPort: 8080
        - name: telemetry
          containerPort: 8081
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

### Environment Variables

  - **POD\_NAME** - Pod name (for automatic sharding in StatefulSet)
  - **POD\_NAMESPACE** - Pod namespace (for automatic sharding in StatefulSet)
  - **NODE\_NAME** - Node name (for node-specific pod metrics in DaemonSet)

This image exposes the following ports:

  - **8080** - HTTP metrics endpoint (`/metrics`)
  - **8081** - Telemetry endpoint (self-monitoring metrics)

### Volumes

  - **/config** - Configuration directory (optional, for kubeconfig or custom resource state configs)

## Command Line Arguments

The `kube-state-metrics` server supports various command-line arguments for configuration, which can be passed via the `args` field in your Kubernetes manifests. Here are the most commonly used ones:

### Resource Configuration

  - `--resources` - Comma-separated list of resources to be enabled (default: all resources)
      - Example: `--resources=pods,deployments,nodes`
  - `--namespaces` - Comma-separated list of namespaces to monitor (default: all namespaces)
  - `--namespace` - Single namespace to monitor (alternative to `--namespaces`)

### Metrics Configuration

  - `--metric-allowlist` - Comma-separated list of metrics to expose (default: all metrics)
  - `--metric-denylist` - Comma-separated list of metrics to exclude
  - `--metric-labels-allowlist` - Comma-separated list of additional Kubernetes label keys to expose as labels
      - Format: `resource=[label1,label2],resource2=[*]`

### Sharding Configuration

  - `--shard` - Shard ordinal (zero-indexed) for horizontal sharding
  - `--total-shards` - Total number of shards for horizontal sharding
  - `--pod` - Pod name for automatic shard discovery in StatefulSet
  - `--pod-namespace` - Pod namespace for automatic shard discovery

### Node-Specific Configuration

  - `--node` - Node name for filtering pod metrics (used in DaemonSet deployments)
  - `--track-unscheduled-pods` - Track pods that are not scheduled to any node

### Network Configuration

  - `--host` - Host to expose metrics on (default: `::`)
  - `--port` - Port to expose metrics on (default: `8080`)
  - `--telemetry-host` - Host to expose telemetry on (default: `::`)
  - `--telemetry-port` - Port to expose telemetry on (default: `8081`)

### Kubernetes API Configuration

  - `--kubeconfig` - Path to kubeconfig file for Kubernetes API access
  - `--apiserver` - Override the API server address in kubeconfig
  - `--use-apiserver-cache` - Use API server cache to reduce latency and etcd load

### Logging Configuration

  - `--log` - Log level (debug, info, warn, error, fatal, panic) (default: `info`)
  - `--enable-gzip-encoding` - Enable gzip encoding for /metrics endpoint

### Advanced Configuration

  - `--custom-resource-state-config` - Inline custom resource state configuration
  - `--custom-resource-state-config-file` - Path to custom resource state configuration file
  - `--custom-resource-state-only` - Only expose custom resource state metrics

### Examples of Common Flags

Monitor specific resources only:
`kube-state-metrics --resources=deployments,pods,statefulsets`

Monitor specific namespaces:
`kube-state-metrics --namespaces=production,staging`

Enable sharding (instance 0 of 3):
`kube-state-metrics --shard=0 --total-shards=3`

Expose only specific metrics:
`kube-state-metrics --metric-allowlist=kube_pod_info,kube_deployment_status_replicas`

## Health Checks

`kube-state-metrics` provides built-in health check endpoints:

  - `/healthz` - Returns 200 if the application is running (startup probe)
  - `/livez` - Returns 200 if the application is not affected by a Kubernetes API outage (liveness probe)
  - `/readyz` - Returns 200 if the application is ready to serve metrics (readiness probe)

Example health check configuration:

```yaml
livenessProbe:
  httpGet:
    path: /livez
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 10
readinessProbe:
  httpGet:
    path: /readyz
    port: 8081
  initialDelaySeconds: 5
  periodSeconds: 10
```

## Metrics Endpoint

All metrics are exposed at the `/metrics` endpoint on port 8080. The metrics are available in Prometheus text format and can be scraped by Prometheus or any compatible monitoring system.

Example metrics:

```
kube_pod_info{namespace="default",pod="example-pod",host_ip="10.0.0.1"} 1
kube_pod_status_phase{namespace="default",pod="example-pod",phase="Running"} 1
kube_deployment_status_replicas{namespace="default",deployment="example"} 3
kube_node_status_condition{node="node-1",condition="Ready",status="true"} 1
```

## Prometheus Integration

Configure Prometheus to scrape `kube-state-metrics`:

```yaml
scrape_configs:
- job_name: 'kube-state-metrics'
  static_configs:
  - targets: ['kube-state-metrics.kube-system.svc.cluster.local:8080']
  metric_relabel_configs:
  - action: labeldrop
    regex: (uid|pod_ip)
```

For Kubernetes service discovery:

```yaml
scrape_configs:
- job_name: 'kube-state-metrics'
  kubernetes_sd_configs:
  - role: service
  relabel_configs:
  - source_labels: [__meta_kubernetes_service_label_app_kubernetes_io_name]
    action: keep
    regex: kube-state-metrics
  - source_labels: [__meta_kubernetes_service_port_name]
    action: keep
    regex: http-metrics
```

## Security

This image runs as the `nobody` user (non-root) for enhanced security. The container follows security best practices and is built on a minimal Debian 12 Slim base image.

## Resource Recommendations

Based on cluster size, recommended resource allocations are:

  - **Small clusters (\< 100 nodes)**:

      - CPU: 100m request, 200m limit
      - Memory: 150Mi request, 300Mi limit

  - **Medium clusters (100-500 nodes)**:

      - CPU: 200m request, 500m limit
      - Memory: 250Mi request, 500Mi limit

  - **Large clusters (\> 500 nodes)**:

      - CPU: 500m request, 1000m limit
      - Memory: 500Mi request, 1Gi limit

**Note:** If you experience high memory usage or CPU throttling, consider implementing horizontal sharding.

## Scaling with Sharding

For large clusters, `kube-state-metrics` can be horizontally scaled using sharding. Sharding distributes the workload across multiple instances by using an md5 hash of each object's UID.

Benefits:

  - Reduced memory consumption per instance (1/n of unsharded setup)
  - Lower latency per instance
  - Better distribution of API server load

Considerations:

  - All instances still receive all API traffic (filtering happens in-memory)
  - Requires monitoring to ensure all shards are healthy
  - StatefulSet-based auto-sharding simplifies management

## Performance Tuning

For optimal performance:

  - Use `--use-apiserver-cache` to reduce latency and etcd load
  - Implement sharding for clusters with \> 500 nodes
  - Use `--metric-allowlist` to reduce cardinality
  - Ensure adequate CPU allocation to prevent queue buildup
  - Monitor the telemetry endpoint for performance metrics

## Contributing and Issues

We'd love for you to contribute\! You can request new features, report bugs, or submit a pull request with your contribution to this image on the SourceMation GitHub repository.

  - [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
  - [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/kube-state-metrics` image is not affiliated with the Kubernetes project. The respective companies and organisations own the trademarks mentioned in the offering. The `sourcemation/kube-state-metrics` image is a separate project and is maintained by [SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on the [SourceMation platform](https://www.sourcemation.com/).

For more information, check out the [kube-state-metrics documentation](https://github.com/kubernetes/kube-state-metrics/tree/main/docs).

### Licenses

The base license for the solution (kube-state-metrics) is the [Apache License 2.0](https://github.com/kubernetes/kube-state-metrics/blob/main/LICENSE). The licenses for each component shipped as part of this image can be found on [the image's appropriate SourceMation entry](https://www.sourcemation.com/).
