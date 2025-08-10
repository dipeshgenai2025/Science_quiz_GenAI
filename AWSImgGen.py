###############################################################################
# AWS Titan Image Generator Wrapper
# 
# Desc: This script provides a thread-safe class-based interface to generate
# images using Amazon Titan Image Generator via AWS Bedrock. The original
# functions have been modified to be stateless and thread-safe.
# 
# Author: Dipesh Karmakar
# Date: 07/08/2025
# License: MIT License
###############################################################################

# Import necessary libraries
import base64
import boto3
import json
import os
import random
import uuid

class AWSImgGen:
    """
    AWSImgGen provides methods to generate images using Amazon Titan Image Generator via AWS Bedrock.
    This version is designed to be thread-safe, making it suitable for multi-user services.
    The original methods now pass data directly to ensure each request is a self-contained operation.
    """

    def __init__(self, region_name="us-east-1", output_dir="output"):
        """
        Initializes the AWSImgGen object.
        Sets up the Bedrock client, model ID, and output directory.
        Creates the output directory if it does not exist.
        """
        # AWS Bedrock client
        self.client = boto3.client("bedrock-runtime", region_name=region_name)
        # Titan model ID
        self.model_id = "amazon.titan-image-generator-v1"
        # Directory to save generated images
        self.output_dir = output_dir

        # Create output directory if needed
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_image(self, prompt: str) -> str:
        """
        Generates an image from a given prompt and saves it to a unique file.
        This method is thread-safe as it does not rely on shared instance state
        between calls and uses a unique ID for the filename.

        Args:
            prompt (str): The text prompt to generate the image from.

        Returns:
            str: The file path of the saved image.
        """
        # Generate a new random seed for each image generation request
        seed = random.randint(0, 2147483647)

        # Prepare the request payload for the Titan model
        native_request = {
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {"text": prompt},
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "quality": "standard",
                "cfgScale": 8.0,
                "height": 512,
                "width": 512,
                "seed": seed,
            },
        }

        # Serialize request to JSON and invoke the model
        request = json.dumps(native_request)
        response = self.client.invoke_model(modelId=self.model_id, body=request)

        # Parse response body
        model_response = json.loads(response["body"].read())
        
        # Get base64 image string
        base64_image_data = model_response["images"][0]
        
        # Decode base64 to bytes
        image_data = base64.b64decode(base64_image_data)

        # Generate a unique filename using UUID to prevent race conditions
        unique_id = uuid.uuid4()
        image_path = os.path.join(self.output_dir, f"aws_image_{unique_id}.png")

        # Save image to file
        with open(image_path, "wb") as file:
            file.write(image_data)
        
        print(f"The generated image has been saved to {image_path}")
        return image_path
