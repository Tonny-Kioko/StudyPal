resource "aws_wafv2_ip_set" "block_ip_set" {
    name = "${var.env}-block-ip-set"
    scope = "REGIONAL"
    ip_address_version = "IPV4"
    addresses = [
        "106.214.95.140/32"
    ]
    description = "WAF will block the specific IP address"
}

resource "aws_wafv2_web_acl" "main_acl" {
    name = "${var.env}-web-acl"
    scope = "REGIONAL"
    description = "Web ACL with IP blocking rules for the ALB"

    default_action {
      allow {}
    }

    rule {
      name = "BlockSpecificIPs"
      priority = 1
      action {
        block{}
      }
      statement {
        ip_set_reference_statement {
          arn = aws_wafv2_ip_set.block_ip_set.arn
        }
      }
      visibility_config {
        cloudwatch_metrics_enabled = true
        metric_name = "BlockSoecificIPs"
        sampled_requests_enabled = true
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name = "${var.env}-web-acl"
      sampled_requests_enabled = true
    }

    tags = {
      name = "${var.env}-webACL"
    }
  
}