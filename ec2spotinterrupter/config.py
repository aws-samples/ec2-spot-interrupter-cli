import boto3

class config:
    ESI_FIS_IAM_POLICY_KEY = "CreatedByESI_FISPolicy"
    ESI_FIS_IAM_ROLE_KEY = "CreatedByESI_FISRole"
    ESI_REGION = ""
    ESI_ACCOUNT = ""

    @staticmethod
    def init():
        session = boto3.session.Session()
        
        config.ESI_REGION = session.region_name
        if not config.ESI_REGION:
            print('Please set aws region!')
            return False

        config.ESI_ACCOUNT = boto3.client('sts').get_caller_identity().get('Account')
        if not config.ESI_ACCOUNT:
            print('Please set aws account id!')
            return False

        print(f'Connected to AWS region: {config.ESI_REGION}, account: {config.ESI_ACCOUNT}')
        
        return True

