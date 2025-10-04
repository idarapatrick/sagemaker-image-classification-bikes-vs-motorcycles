import json
import boto3
import base64

ENDPOINT = 'image-classification-2025-10-04-08-34-38-274'  # deployed endpoint name

runtime = boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    
    # Decode the image data
    image = base64.b64decode(event['body']['image_data'])

    # Instantiate a Predictor
    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT,
        ContentType='image/png',
        Body=image
    )
    
    # Make a prediction
    inferences = json.loads(response['Body'].read().decode())
    
    # We return the data back to the Step Function    
    event["inferences"] = inferences
    return {
        'statusCode': 200,
        'body': event
    }