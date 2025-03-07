# macOS AI Screenshot Renamer

A Python script that extracts text, generates AI captions, and intelligently renames macOS screenshots using OCR and LLMs.

---

## 📌 Get Running

### 1️⃣ Install Required Dependencies

#### Install Homebrew (if not installed)
If you haven't installed Homebrew yet, run:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Install system dependencies (macOS):
```bash
brew install ollama exiftool vips
```

#### Install Python dependencies:
```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

### 1️⃣ Start the Ollama Server

Before running the script, start the Ollama server:
```bash
ollama serve
```

### 2️⃣ Run the Ollama Unit Test
Before processing screenshots, verify that the LLM is working properly:
```bash
./screenshot-renamer.py -t
```
Example Output:
```
Selected Ollama model: phi4:14b-q8_0
Running unit test...
Ollama completed in 2.38 seconds
SUCCESS! 95 + 48 = 143
```

### 3️⃣ Run in Dry-Run Mode (Preview Changes)
```bash
./screenshot-renamer.py --dry-run
```
> Dry-run mode: Shows how images would be renamed without making changes.

### 4️⃣ Run Normally (Modify Files)
```bash
./screenshot-renamer.py
```
> This will rename and update metadata for all screenshots in `~/Desktop` by default.

---

## 📌 Usage Help

```bash
./screenshot-renamer.py -h
```

### Command-Line Options:
```
usage: screenshot-renamer.py [-h] [-n] [-t] [directory]

Batch process images with step-by-step feedback.

positional arguments:
  directory        Directory containing images (default: ~/Desktop)

options:
  -h, --help       Show this help message and exit.
  -n, --dry-run    Perform a dry run without modifying files.
  -t, --unit-test  Run a unit test (ask LLM to add two numbers).
```

---

## 🔧 How It Works

1. Finds macOS screenshots in the specified directory.
2. Extracts text from the screenshot using OCR.
3. Generates a caption using AI (**Moondream2**).
4. Creates a smart filename using an LLM (**Ollama**).
5. Renames the file, prefixing it with the original date (`screenshot_YYYY-MM-DD`).
6. Writes metadata (OCR text & AI caption) into the image’s EXIF.

---

## 📌 Example Before & After

### **Original macOS Screenshot:**
```
Screenshot_2025-01-09_at_6.16.30_PM.png
```

### **AI Processed Filename:**
```
screenshot_2025-01-09-wifi_networking_interface_details.png
```

---

## 🛠 Troubleshooting

### Ollama Server Not Running

If you see an error related to **Ollama not responding**, start the server:
```bash
ollama serve
```

### Model Not Found (`ollama._types.ResponseError: model not found`)
If you see an error like:
```bash
ollama._types.ResponseError: model "llama3.2:3b-instruct-q5_K_M" not found, try pulling it first (status code: 404)
```
Run the following command to download the required model:
```bash
ollama pull llama3.2:3b-instruct-q5_K_M
```
This ensures the correct model is available for processing.

### Selecting the Right Ollama Model
The script automatically selects the best Ollama model based on available VRAM:

| VRAM Size      | Model Used                          |
|---------------|--------------------------------|
| **>30GB**     | `phi4:14b-q8_0`               |
| **>14GB**     | `phi4:14b-q4_K_M`             |
| **>4GB**      | `llama3.2:3b-instruct-q5_K_M` |
| **Default**   | `llama3.2:1b-instruct-q4_K_M` |

If your system **lacks VRAM**, you may need to manually select a smaller model by running:
```bash
ollama pull llama3.2:1b-instruct-q4_K_M
```
Then update `config_ollama.py` to force using that model.

---

## 🔗 Resources

- **[Ollama Documentation](https://ollama.com/docs)**
- **[Ollama Phi Model](https://ollama.com/library/phi)**
- **[Moondream2 Model](https://huggingface.co/vikhyatk/moondream2)**
- **[Homebrew Documentation](https://brew.sh/)**
- **[ExifTool Documentation](https://exiftool.org/)**

---

## 📌 Contributing

Pull requests are welcome! Open an issue if you encounter bugs or have feature requests.

---

## 📜 License

This project is licensed under the **GPL v3.0**.
