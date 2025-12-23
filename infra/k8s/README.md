Kubernetes manifests

Base resources run the workbench as Jobs and CronJobs and can mount persistent storage for run directories.

Layout
- base: namespace, RBAC, config, CronJob
- overlays: local and prod variants
