locals {
  bucket = var.bucket
}

resource "aws_s3_bucket_public_access_block" "var_bucket" {
  bucket                  = local.bucket
  block_public_acls       = var.block_public_acls
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket" "example" {
  bucket = "example"
}
