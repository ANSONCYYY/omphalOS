Terraform infrastructure

This tree provisions a minimal cloud footprint for storing runs, publishing release bundles, and operating scheduled execution.

Layout
- main.tf, variables.tf, outputs.tf: root module
- modules: composable components
- env: environment overlays that pin variables for dev and prod
