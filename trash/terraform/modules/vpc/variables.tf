variable "vpc" {
    description = "VPC CIDR"
    type = object({
        NAME = string,
        CIDR = string
    })
}

variable "subnets" {
    description = "VPC CIDR"
    type = list(object({
        AZ_ORDER = number,
        NAME = string,
        CIDR = string
    }))
}

variable "availability_zones" {
    description = "VPC CIDR"
    type = list(string)
}