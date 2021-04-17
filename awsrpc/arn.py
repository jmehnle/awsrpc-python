from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum


# <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>
class AWSPartition(Enum):
    AWS = "aws"
    AWS_CN = "aws-cn"
    AWS_US_GOV = "aws-us-gov"

    @classmethod
    def for_value(cls, value: str) -> AWSPartition:
        candidates = [m for m in cls if m.value == value]
        if not candidates:
            values = [m.value for m in cls]
            raise ValueError(f"Unknown {cls.__name__} member value: {value!r}, must be one of: {values!r}")
        return candidates[0]


# <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>
@dataclass
class ARN:
    partition: AWSPartition = AWSPartition.AWS
    service: Optional[str] = None
    region: Optional[str] = None
    account_id: Optional[str] = None
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None

    PATTERN = re.compile(
        r"""
            arn :
            (?P<partition>[^:]+)?      :
            (?P<service>[^:]+)?        :
            (?P<region>[^:]+)?         :
            (?P<account_id>[^:]+)?     :
          ( (?P<resource_type>[^:/]+) [:/] )?
            (?P<resource_id>.+)?
        """,
        re.X
    )

    @classmethod
    def parse(cls, arn_str: str) -> ARN:
        match = cls.PATTERN.fullmatch(arn_str)
        if not match:
            raise ValueError(
                f"ARN must match 'arn:<partition>:<service>:<region>:<account-id>:<resource_id>', got: {arn_str!r}"
            )
        attrs = match.groupdict()
        if attrs["partition"]:
            attrs["partition"] = AWSPartition.for_value(attrs["partition"])
        return cls(**attrs)

    def __str__(self) -> str:
        partition_str = self.partition.value
        service_str = self.service or ""
        region_str = self.region or ""
        account_id_str = self.account_id or ""
        if self.resource_type:
            resource_str = f"{self.resource_type}/{self.resource_id}"
        else:
            resource_str = self.resource_id or ""
        return f"arn:{partition_str}:{service_str}:{region_str}:{account_id_str}:{resource_str}"
