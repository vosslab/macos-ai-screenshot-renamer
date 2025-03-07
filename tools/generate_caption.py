#!/usr/bin/env python3

import torch
import time
from PIL import Image
from transformers import AutoTokenizer, AutoModelForCausalLM

from tools import common_func

def generate_caption(image_path: str, ai_components: dict) -> str:
	"""
	Generate a caption for a given image using Moondream2.

	Args:
		image_path (str): Path to the image file.
		ai_components (dict): Dictionary containing the model, tokenizer, device, and prompt.

	Returns:
		str: The generated caption.
	"""
	image = Image.open(image_path)
	image = common_func.resize_image(image, 720)  # Reduce to 720px max

	# Ensure image is on the correct device
	image = image.convert("RGB")

	start_time = time.time()

	if ai_components['prompt'] is None:
		caption_result = ai_components['model'].caption(image, length="normal")
		caption = caption_result.get("caption", "")
	else:
		caption_result = ai_components['model'].query(image, ai_components['prompt'])
		caption = caption_result.get("answer", "")

	print(f"Time taken for caption generation: {time.time() - start_time:.2f} seconds")

	if not caption:
		raise ValueError("Caption generation failed. The model returned an empty response.")

	return caption

#============================================
def generate_caption2(image_path: str, ai_components: dict) -> str:
	"""
	Generate a caption for a given image using Moondream2.

	Args:
		image_path (str): Path to the image file.
		ai_components (dict): Dictionary containing the model, tokenizer, device, and prompt.

	Returns:
		str: The generated caption.
	"""
	image = Image.open(image_path)
	image = common_func.resize_image(image, 1280)

	if ai_components['prompt'] is None:
		caption_result = ai_components['model'].caption(image, length="normal")
		caption = caption_result.get("caption", "")
	else:
		caption_result = ai_components['model'].query(image, ai_components['prompt'])
		caption = caption_result.get("answer", "")

	if not caption:
		raise ValueError("Caption generation failed. The model returned an empty response.")

	return caption

#============================================
def setup_ai_components(prompt: str = None):
	"""
	Setup AI components, loading Moondream2 model and tokenizer.

	Args:
		prompt (str): Custom AI prompt, optional.

	Returns:
		dict: AI model components (model, tokenizer, device, prompt).
	"""
	model_id = "vikhyatk/moondream2"
	revision = "2025-01-09"
	device = common_func.get_mps_device()

	model = AutoModelForCausalLM.from_pretrained(
		model_id,
		trust_remote_code=True,
		revision=revision,
		torch_dtype=torch.float16,
		device_map={"": device},
	)
	tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
	model.to(device)

	return {'model': model, 'tokenizer': tokenizer, 'device': device, 'prompt': prompt}

