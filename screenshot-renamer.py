#!/usr/bin/env python3

import gc
import os
import time
import random
import argparse

import torch

from tools.extract_text import extract_text_from_image
from tools.generate_caption import generate_caption, setup_ai_components
from tools.intelligent_filename import generate_intelligent_filename
from tools.update_metadata import write_exif_metadata


def clear_gpu_memory():
	"""Forcefully clears GPU memory after processing an image to prevent out-of-memory errors."""
	gc.collect()  # Clean Python memory
	if torch.backends.mps.is_available():
		torch.mps.empty_cache()  # Clears MPS (Metal Performance Shaders) memory
		#torch.cuda.empty_cache()  # Just in case some models use CUDA fallback

#============================================
def format_preview(text: str, max_lines: int = 2, line_length: int = 80) -> str:
	"""
	Formats text into a preview with a max number of lines and line length.

	Args:
		text (str): The text to format.
		max_lines (int): The maximum number of lines to show.
		line_length (int): The maximum length per line.

	Returns:
		str: Formatted preview text.
	"""
	words = text.split()
	lines = []
	current_line = ""

	for word in words:
		if len(current_line) + len(word) + 1 > line_length:
			lines.append(current_line)
			current_line = word
			if len(lines) == max_lines:
				break
		else:
			current_line += " " + word if current_line else word

	if current_line and len(lines) < max_lines:
		lines.append(current_line)

	return "\n".join(lines)

import re
import os
import time

def process_image(image_path: str, ai_components: dict, dry_run: bool):
	"""
	Processes a single image: extracts text, generates captions, renames file, and updates metadata.

	Args:
		image_path (str): Path to the image file.
		ai_components (dict): AI model components.
		dry_run (bool): If True, only prints changes without modifying files.
	"""
	filename = os.path.basename(image_path)
	print('\n')
	print('='* 60)
	print(f"Processing image: {filename}")

	start_time = time.time()
	ocr_text = extract_text_from_image(image_path)
	ocr_time = time.time() - start_time
	print(f"\nOCR Results:\n{format_preview(ocr_text)}")
	print(f"Time taken for OCR: {ocr_time:.2f} seconds")

	start_time = time.time()
	ai_caption = generate_caption(image_path, ai_components)
	caption_time = time.time() - start_time
	print(f"\nCaption Results:\n{format_preview(ai_caption)}")
	print(f"Time taken for caption generation: {caption_time:.2f} seconds")

	start_time = time.time()
	new_filename = generate_intelligent_filename(ocr_text, ai_caption)

	# Correctly extract only the date from the filename
	match = re.search(r"(\d{4}-\d{2}-\d{2})", filename, re.IGNORECASE)
	date_part = match.group(1) if match else "unknown-date"

	# Construct the final filename with correct date prefix
	new_filename = f"screenshot_{date_part}-{new_filename}"

	filename_time = time.time() - start_time
	new_path = os.path.join(os.path.dirname(image_path), new_filename)
	print(f"\nAI Filename Result: {new_filename}")
	print(f"Time taken for filename generation: {filename_time:.2f} seconds")

	if dry_run:
		print(f"Dry Run: Would rename '{filename}' -> '{new_filename}'")
	else:
		start_time = time.time()
		os.rename(image_path, new_path)
		write_exif_metadata(new_path, ocr_text, ai_caption)
		metadata_time = time.time() - start_time
		print(f"Renamed and updated metadata: '{filename}' -> '{new_filename}'")
		print(f"Time taken for renaming and metadata update: {metadata_time:.2f} seconds")
	clear_gpu_memory()

#============================================
def process_directory(directory: str):
	"""
	Processes all images in a directory with detailed step-by-step feedback.

	Args:
		directory (str): Path to the directory containing images.
		dry_run (bool): If True, only prints changes without modifying files.
	"""
	image_files = []
	for filename in os.listdir(directory):
		#note macos filesystem are 99% of the time case INsensitive
		lower_filename = filename.lower()
		if not lower_filename.startswith("screen"):
			continue
		extension = os.path.splitext(lower_filename)[-1]
		#if not extension in (".png", ".jpg", ".jpeg"):
		if extension != ".png":
			continue
		image_files.append(lower_filename)

	if not image_files:
		print("No images found in the specified directory.")
		raise FileNotFoundError

	return image_files

#============================================
def parse_args():
	"""
	Parse command-line arguments.
	"""
	parser = argparse.ArgumentParser(description="Batch process images with step-by-step feedback.")
	parser.add_argument("directory", nargs="?", default=os.path.expanduser("~/Desktop"),
						help="Directory containing images (default: ~/Desktop)")
	parser.add_argument("-n", "--dry-run", dest="dry_run", action="store_true",
						help="Perform a dry run without modifying files.")
	parser.add_argument("-t", "--unit-test", dest="unit_test", action="store_true",
						help="Run a unit test (ask LLM to add two numbers).")
	args = parser.parse_args()
	return args

#============================================
def main():
	"""
	Main function
	"""
	args = parse_args()

	if args.unit_test:
		import sys
		from tools import config_ollama
		config_ollama.unit_test()
		sys.exit(0)

	image_files = process_directory(args.directory)
	image_files.sort()
	if args.dry_run is True:
		random.shuffle(image_files)
	else:
		image_files.sort(key=len)

	for i, filename in enumerate(image_files, start=1):
		if i > 9:
			print(f"... plus {len(image_files)-9} more files")
			break
		print(f"{i}: {filename}")

	ai_components = setup_ai_components()
	for i, filename in enumerate(image_files, start=1):
		image_path = os.path.join(args.directory, filename)
		print(f"\nProcessing image {i} of {len(image_files)}")
		process_image(image_path, ai_components, args.dry_run)


if __name__ == "__main__":
	main()
