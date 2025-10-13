import kopf
import kubernetes
import os
from kubernetes import config

try:
    if "KUBERNETES_SERVICE_HOST" in os.environ:
        print("📦 Running inside a Kubernetes cluster.")
        kubernetes.config.load_incluster_config()
    else:
        kubernetes.config.load_kube_config()
        cfg, active_context = config.list_kube_config_contexts()
        print(f"💻 Running locally. Active context: {active_context['name']}")
except kubernetes.config.ConfigException:
    print("⚠️ Could not configure Kubernetes client.")

core = kubernetes.client.CoreV1Api()

@kopf.on.create('bakery.myorg.io', 'v1', 'cakes')
def bake_cake(spec, name, namespace, logger, **_):
    flavor = spec.get('flavor', 'vanilla')
    sleep_s = int(spec.get('bakeTimeSeconds', 5))
    pod = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {"name": f"{name}-baker"},
        "spec": {
            "restartPolicy": "Never",
            "containers": [{
                "name": "baker",
                "image": "busybox:stable",
                "command": ["sh", "-c", f'echo "🎂 Baking {flavor}..." && sleep {sleep_s} && echo "✅ Baked!"']
            }]
        }
    }
    core.create_namespaced_pod(namespace=namespace, body=pod)
    logger.info(f"Started baking '{name}' ({flavor}) for {sleep_s}s.")

@kopf.on.delete('bakery.myorg.io', 'v1', 'cakes')
def cleanup_cake(spec, name, namespace, logger, **_):
    pod_name = f"{name}-baker"
    try:
        core.delete_namespaced_pod(name=pod_name, namespace=namespace)
        logger.info(f"Cleaned up pod {pod_name}.")
    except kubernetes.client.exceptions.ApiException as e:
        if e.status != 404:
            raise
