resource "aws_dynamodb_table" "this" {
  name         = "${var.name_prefix}-run-registry"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "run_id"

  attribute {
    name = "run_id"
    type = "S"
  }

  tags = var.tags
}

output "table_name" {
  value = aws_dynamodb_table.this.name
}
