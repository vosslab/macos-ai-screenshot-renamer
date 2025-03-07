#!/usr/bin/env python3

import argparse
from tools import config_ollama

def generate_intelligent_filename(ocr_text: str, ai_caption: str) -> str:
	"""
	Generates a concise, valid filename using an LLM based on OCR and AI caption.

	Args:
		ocr_text (str): Extracted text from the image.
		ai_caption (str): AI-generated caption.

	Returns:
		str: A valid, concise filename.
	"""
	prompt = (
		"Generate a concise, descriptive filename (max 64 characters) "
		"for a macos screenshot stored as PNG image "
		"based on the given OCR text and AI generated caption. "
		"The filename should give the user a sense of "
		"what the image might used for or its purpose or include something about its content "
		"Prioritize clarity and distinctiveness while avoiding redundancy.\n\n"
		"Format requirements:\n"
		"- The first output is the just the filename\n"
		"- Words must be separated by underscores (_)\n"
		"- No filename extensions (e.g., .png)\n"
		"- No full sentences\n"
		"- No explanations\n"
		"- No special characters (except underscores)\n"
		"- Maximum length: 64 characters\n\n"
		f"OCR Text: {ocr_text}\n\n"
		f"Caption: {ai_caption}\n\n"
		"Filename:"
	)

	response = config_ollama.run_ollama(prompt).strip()

	# Take only the first line in case of multiple responses
	filename = response.split("\n")[0]
	#note macos filesystem are 99% of the time case INsensitive
	filename = filename.lower()
	# Ensure filename is valid (remove special characters, limit length)
	filename = filename.replace(" ", "_").replace("__", "_")
	# Allow only safe characters
	filename = "".join(c for c in filename if c.isalnum() or c in "._-")
	filename = filename[:64]  # Enforce max length
	filename += ".png"  # Append extension

	return filename

#============================================
def main():
	"""
	Main function for standalone execution and unit testing.
	"""
	parser = argparse.ArgumentParser(description="Generate intelligent filenames for images.")
	parser.add_argument("ocr_text", type=str, nargs="?", default="Example OCR Text",
						help="Extracted text from the image.")
	parser.add_argument("ai_caption", type=str, nargs="?", default="Example AI Caption",
						help="AI-generated caption for the image.")
	parser.add_argument("-t", "--test", action="store_true",
						help="Run a unit test (ask LLM 'What is 2+2?').")
	args = parser.parse_args()

	if args.test:
		config_ollama.unit_test()
	else:
		new_filename = generate_intelligent_filename(args.ocr_text, args.ai_caption)
		print(f"Generated Filename: {new_filename}")

if __name__ == "__main__":
	main()
