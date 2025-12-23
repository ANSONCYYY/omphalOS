resource "null_resource" "runtime_identity" {
  triggers = { name = var.name }
}
