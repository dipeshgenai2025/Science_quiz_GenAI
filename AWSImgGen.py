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

    def PromptGeneration(self, prompt: str) -> dict:
        """
        Prepares the request payload for the image generation model using the provided prompt.
        This function is now stateless and returns the request dictionary directly.

        Args:
            prompt (str): The text prompt to generate the image from.

        Returns:
            dict: The request payload for the model.
        """
        # Generate a new random seed for each request
        seed = random.randint(0, 2147483647)
        
        # Prepare the request payload for Titan model
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
        return native_request

    def InvokeModel(self, native_request: dict) -> dict:
        """
        Invokes the Titan image generation model with the prepared request.
        The request payload is passed as an argument, making the method stateless.

        Args:
            native_request (dict): The request payload to send to the model.

        Returns:
            dict: The response from the model.
        """
        # Serialize request to JSON
        request = json.dumps(native_request)
        # Call AWS Bedrock
        response = self.client.invoke_model(modelId=self.model_id, body=request)
        return response

    def ProcessResponse(self, response: dict) -> str:
        """
        Processes the model response, decodes the image, and saves it to the output directory.
        This function now uses a UUID for the filename to avoid collisions.

        Args:
            response (dict): The response from the model invocation.

        Returns:
            str: The file path of the saved image.
        """
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

# Example usage:
if __name__ == "__main__":
    prompt = "A picture of a majestic eagle soaring over snow-capped mountains."
    img_gen = AWSImgGen()  # Create image generator object
    
    # The new, thread-safe sequence of calls
    try:
        # Step 1: Generate the prompt payload
        native_request = img_gen.PromptGeneration(prompt)
        
        # Step 2: Invoke the model with the payload
        response = img_gen.InvokeModel(native_request)
        
        # Step 3: Process the response and save the image
        image_file_path = img_gen.ProcessResponse(response)
        
        print(f"Image successfully generated and saved at: {image_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
