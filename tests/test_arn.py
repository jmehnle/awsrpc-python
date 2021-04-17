import pytest

from awsrpc.arn import AWSPartition, ARN


class TestAWSPartition:
    def test_members(self):
        AWSPartition.AWS
        AWSPartition.AWS_CN
        AWSPartition.AWS_US_GOV

    def test_for_value(self):
        for value in ('aws', 'aws-cn', 'aws-us-gov'):
            member = AWSPartition.for_value(value)
            assert member.value == value

        with pytest.raises(ValueError):
            AWSPartition.for_value('foobar')


class TestARN:
    @pytest.fixture
    def arn(self):
        return ARN(
            partition=AWSPartition.AWS,
            service='iam',
            region='us-west-2',
            account_id='1234',
            resource_type='user',
            resource_id='julian'
        )

    def test_init(self, arn):
        test_arn = ARN(
            partition=arn.partition,
            service=arn.service,
            region=arn.region,
            account_id=arn.account_id,
            resource_type=arn.resource_type,
            resource_id=arn.resource_id,
        )
        assert test_arn == arn

    def test_parse(self, arn):
        test_arn = ARN.parse('arn:aws:iam:us-west-2:1234:user/julian')
        assert test_arn == arn

    def test_str(self, arn):
        assert str(arn) == 'arn:aws:iam:us-west-2:1234:user/julian'
