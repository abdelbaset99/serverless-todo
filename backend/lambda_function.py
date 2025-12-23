import json
import boto3
import uuid
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TodoTable')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    print(event)
    
    http_method = event['httpMethod']
    
    # These headers allow ANY origin to make ANY request
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE",
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token"
    }

    try:
        # --- NEW: Handle OPTIONS (Preflight) explicitly ---
        if http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps('CORS OK')
            }

        # --- GET: List all items ---
        if http_method == 'GET':
            response = table.scan()
            items = response.get('Items', [])
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(items, cls=DecimalEncoder)
            }

        # --- POST: Create a new item ---
        elif http_method == 'POST':
            body = json.loads(event['body'])
            item_id = str(uuid.uuid4())
            item = {
                'id': item_id,
                'task': body['task'],
                'status': 'pending'
            }
            table.put_item(Item=item)
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(item)
            }

        # --- PUT: Update item ---
        elif http_method == 'PUT':
            body = json.loads(event['body'])
            item_id = body['id']
            
            update_expression = []
            expression_values = {}
            expression_names = {}

            if 'task' in body:
                update_expression.append("task = :t")
                expression_values[':t'] = body['task']

            if 'status' in body:
                update_expression.append("#st = :s")
                expression_values[':s'] = body['status']
                expression_names['#st'] = 'status'

            if not update_expression:
                return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'message': 'No fields'})}

            cmd = {
                'Key': {'id': item_id},
                'UpdateExpression': 'SET ' + ', '.join(update_expression),
                'ExpressionAttributeValues': expression_values,
                'ReturnValues': "UPDATED_NEW"
            }
            if expression_names:
                cmd['ExpressionAttributeNames'] = expression_names

            response = table.update_item(**cmd)

            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(response['Attributes'], cls=DecimalEncoder)
            }

        # --- DELETE: Remove an item ---
        elif http_method == 'DELETE':
            body = json.loads(event['body'])
            table.delete_item(Key={'id': body['id']})
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'Item deleted'})
            }
            
        else:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'message': 'Unsupported method'})
            }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
