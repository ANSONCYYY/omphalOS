terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

module "artifact_bucket" {
  source      = "./modules/artifact_bucket"
  name_prefix = var.name_prefix
  tags        = var.tags
}

module "run_registry" {
  source      = "./modules/run_registry"
  name_prefix = var.name_prefix
  tags        = var.tags
}
