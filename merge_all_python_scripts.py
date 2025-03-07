#!/bin/bash

# Output file
OUTPUT_FILE="merged_python_scripts.txt"

# Clear the output file if it exists
> "$OUTPUT_FILE"

# Find and merge all Python files
find . -type f -name "*.py" | while read -r file; do
    echo "Processing $file"
    echo -e "\n### FILE: $file ###\n" >> "$OUTPUT_FILE"
    cat "$file" >> "$OUTPUT_FILE"
    echo -e "\n### END OF $file ###\n" >> "$OUTPUT_FILE"
done

echo "Merged all Python files into $OUTPUT_FILE"
