locals {
  locals_env = {
    env             = "dev"
    resource_prefix = "${local.locals_cmn.project_name}-dev"
    table_prefix    = "${local.locals_cmn.project_name}_dev"
    sagemaker_unified_studio = {
      default_glue_database  = "glue_db_bsyeydfwn7q7bt"
      default_glue_s3_bucket = "amazon-sagemaker-084700548016-ap-northeast-1-c9c6724fb892"
      default_glue_data_path = "dzd_cdnvozc1kuwhqx/cizbreydejg5cp/dev/data/catalogs"
      network = {
        vpcid               = "vpc-0a674b3319ee58a84"
        ngw_subnet          = "subnet-0bcb85a021c83be03"
        private_route_table = "rtb-01410edc7a5e47a07"
      }
    }
  }
}