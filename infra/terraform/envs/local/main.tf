module "artifact_store" {
  source = "../../modules/artifact_store"
  name = "omphalos-artifacts-local"
  retention_days = 30
}

module "runtime_identity" {
  source = "../../modules/runtime_identity"
  name = "omphalos-runtime-local"
}
