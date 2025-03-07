#!/usr/bin/env python3

import os
import time
import torch
from PIL import Image

#============================================
def get_mps_device():
	"""
	Detects the best available device for computation.
	Returns "mps" for Apple Silicon, "cuda" for NVIDIA, or "cpu" as fallback.
	"""
	if torch.backends.mps.is_available():
		return "mps"
	raise NotImplementedError
	if torch.cuda.is_available():
		return "cuda"
	return "cpu"

def resize_image(image: Image.Image, max_dimension: int) -> Image.Image:
	"""
	Resizes an image while maintaining its aspect ratio.

	Args:
		image (PIL.Image): Input image.
		max_dimension (int): Maximum width or height.

	Returns:
		PIL.Image: Resized image.
	"""
	width, height = image.size
	if max(width, height) <= max_dimension:
		return image

	if width > height:
		new_width = max_dimension
		new_height = int((height / width) * max_dimension)
	else:
		new_height = max_dimension
		new_width = int((width / height) * max_dimension)

	# Use LANCZOS instead of the removed ANTIALIAS
	return image.resize((new_width, new_height), Image.LANCZOS)

#============================================
def get_image_paths(directory: str):
	"""
	Returns a list of image file paths in a directory.

	Args:
		directory (str): Path to directory.

	Returns:
		list: List of image file paths.
	"""
	return [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
