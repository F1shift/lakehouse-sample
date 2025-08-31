# resource "aws_lakeformation_permissions" "aurora_database_permissions" {
#   principal        = "arn:aws:iam::084700548016:user/f1shift"
#   permissions      = ["SUPER_USER"]
#   catalog_resource = true
#   catalog_id       = "${data.aws_caller_identity.current.account_id}:lakehouse_sample_mysql_2"
# }
# ----上記でうまくいかないため、代わりにAWS CLIで設定する

locals {
  permission = {
    Principal = {
      DataLakePrincipalIdentifier = "${var.locals_env.administrator_user}"
    },
    Resource = {
      Catalog = {
        Id = "084700548016:lakehouse_sample_mysql_2"
      }
    },
    Permissions = [
      "ALL",
      "SUPER_USER"
    ],
    PermissionsWithGrantOption = [
      "ALL"
    ]
  }
}

resource "null_resource" "example" {
  provisioner "local-exec" {
    command = "aws lakeformation grant-permissions --cli-input-json '${jsonencode(local.permission)}'"
  }
}