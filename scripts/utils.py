import json
import boto3
import pdb


def write_json(filepath, data, mode='w'):
    with open(filepath, mode, encoding='utf-8') as outfile:
        json.dump(data, outfile)


def read_json(filepath, mode='r'):
    with open(filepath, mode, encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data


class aws_dynamodb:
    def __init__(self, profile_name="jw_fake", table_name='speech_table'):
        self.__dynamodb = boto3.session.Session(
            profile_name=profile_name).resource('dynamodb', endpoint_url='http://localhost:8000')
        self.__table_name = table_name
        self.__table = self.__dynamodb.Table(self.__table_name)

    # should fail if item already exists in DB
    def put_item(self, data_dict):
        self.__table.put_item(
            Item=data_dict
        )

    def get_item(self, key):
        get_response = self.__table.get_item(
            Key={'speech_id': key}
        )
        item = get_response['Item']
        return item

    def check_key(self, key):
        """Returns True if key in DB returns False if key not in DB"""
        try:
            self.get_item(key)
            return True
        except:
            return False

    # need to be able to update arbitrary set of attributes
    # def update_item(self, key):
    #     update_response = self.__table.update_item(
    #         Key={'speech_id': key}
    #     )
    #     return None

    def get_keys(self):
        scan_response = self.__table.scan(
            AttributesToGet=[
                'speech_id',
            ],
        )
        items = scan_response['Items']
        while 'LastEvaluatedKey' in scan_response:
            scan_response = self.__table.scan(
                AttributesToGet=[
                    'speech_id',
                ],
                ExclusiveStartKey=scan_response['LastEvaluatedKey']
            )
            items += scan_response['Items']

        key_list = [item['speech_id'] for item in items]
        return key_list

    def create_table(self):
        self.__dynamodb.create_table(
            TableName=self.__table_name,
            KeySchema=[
                {
                    'AttributeName': 'speech_id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'speech_id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )

    def delete_table(self):
        self.__table.delete()


if __name__ == '__main__':
    dynamodb = aws_dynamodb()
    dynamodb.create_table()
