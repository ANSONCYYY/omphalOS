resource "null_resource" "artifact_store" {
  triggers = {
    name = var.name
    retention_days = tostring(var.retention_days)
  }
}
