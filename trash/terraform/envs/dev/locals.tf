locals {
    ENVIREMENT  = "dev"
    MAIN_REGION = "ap-northeast-1"
    PREFIX    = "lakehouse-sample"
}

locals {
    MAIN = {
        VPC = {
            NAME = "lakehouse-sample-vpc-${local.ENVIREMENT}-main"
            CIDR = "10.0.0.0/16"
        }
        SUBNETS = [
            {
                AZ_ORDER = 0
                NAME     = "public-subnet-1"
                CIDR     = "10.0.0.0/24"
            },
            {
                AZ_ORDER = 1
                NAME     = "public-subnet-2"
                CIDR     = "10.0.1.0/24"
            },
            {
                AZ_ORDER = 0
                NAME     = "private-subnet-1"
                CIDR     = "10.0.2.0/24"
            },
            {
                AZ_ORDER = 1
                NAME     = "private-subnet-2"
                CIDR     = "10.0.3.0/24"
            }
        ]
    }
}