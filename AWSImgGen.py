###############################################################################
# AWS Titan Image Generator Wrapper
# 
# Desc: This script provides a class-based interface to generate images using
# Amazon Titan Image Generator via AWS Bedrock.
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

class AWSImgGen:
    """
    AWSImgGen provides methods to generate images using Amazon Titan Image Generator via AWS Bedrock.
    Handles prompt creation, model invocation, and image saving.
    """

    def __init__(self, region_name="us-east-1", output_dir="output"):
        """
        Initializes the AWSImgGen object.
        Sets up the Bedrock client, model ID, output directory, random seed, and request template.
        Creates the output directory if it does not exist.
        """
        # AWS Bedrock client
        self.client = boto3.client("bedrock-runtime", region_name=region_name)
        # Titan model ID
        self.model_id = "amazon.titan-image-generator-v1"
        # Directory to save generated images
        self.output_dir = output_dir
        # Random seed for image generation
        self.seed = random.randint(0, 2147483647)
        # Placeholder for the request payload
        self.native_request = None

        # Create output directory if needed
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def PromptGeneration(self, prompt):
        """
        Prepares the request payload for the image generation model using the provided prompt.
        Args:
            prompt (str): The text prompt to generate the image from.
        """
        # Prepare the request payload for Titan model
        self.native_request = {
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {"text": prompt},
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "quality": "standard",
                "cfgScale": 8.0,
                "height": 512,
                "width": 512,
                "seed": self.seed,
            },
        }

    def InvokeModel(self):
        """
        Invokes the Titan image generation model with the prepared request.
        Returns:
            dict: The response from the model.
        Raises:
            ValueError: If the prompt has not been generated yet.
        """
        # Check if prompt is generated
        if not self.native_request:
            raise ValueError("Prompt not generated. Call PromptGeneration() first.")
        # Serialize request to JSON
        request = json.dumps(self.native_request)
        # Call AWS Bedrock
        response = self.client.invoke_model(modelId=self.model_id, body=request)
        return response

    def ProcessResponse(self, response):
        """
        Processes the model response, decodes the image, and saves it to the output directory.
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

        # Find a unique filename
        i = 1
        while os.path.exists(os.path.join(self.output_dir, f"aws_image_{i}.png")):
            i += 1
        image_path = os.path.join(self.output_dir, f"aws_image_{i}.png")
        # Save image to file
        with open(image_path, "wb") as file:
            file.write(image_data)
        print(f"The generated image has been saved to {image_path}")
        return image_path

# Example usage:
if __name__ == "__main__":
    prompt = "A picture of human only male reproductive organ."
    img_gen = AWSImgGen()  # Create image generator object
    img_gen.PromptGeneration(prompt)  # Prepare the prompt
    response = img_gen.InvokeModel()  # Invoke the model
    img_gen.ProcessResponse(response)  # Process