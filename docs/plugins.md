# Plugins

omphalOS is designed to keep integrations out of the core. The core enforces contracts; plugins provide real-world I/O.

## What plugins can provide

- Connectors (read inputs)
- Exporters (write additional products)
- Lineage sinks (forward lineage to external systems)

## Plugin boundary principles

- A plugin must be explicit about whether it is compatible with hermetic execution.
- Plugins must not mutate finalized artifacts.
- Plugins should only write through the artifact store APIs so fingerprints and manifests stay correct.

## Discovery

Plugins are discovered via Python entry points. The core loads available entry points and validates interface versions before use.

## Security posture

Plugins are code execution. Treat them as trusted code and gate them like any other dependency:

- pin versions
- review changes
- include plugin artifacts in publishability scans when distributing bundles
