variable "region" {
  type    = string
  default = "us-east-1"
}

variable "name_prefix" {
  type    = string
  default = "omphalos"
}

variable "tags" {
  type    = map(string)
  default = {}
}
