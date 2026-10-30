# Google Maps Scraper

A robust, asynchronous web scraping tool built with **Python** and **Playwright** to extract local business leads (names, phone numbers, websites, ratings, reviews, etc.) from Google Maps based on custom search queries and locations.

## 📁 Project Directory Structure

The project follows a clean, modular architecture to separate configuration, core processing logic, inputs, and outputs:

google-maps-scrapper/
│
├── config/                      # 📁 Configuration settings & selectors
│   └── config.py                # Centralized CSS selectors and constants
│
├── data/                        # 📁 Master JSON inputs & datasets
│   ├── businesses.json          # Production business categories
│   ├── locations.json           # Production US locations
│   ├── dummybusinesses.json     # Minimal test businesses for quick dry runs
│   └── dummylocations.json      # Minimal test locations
│
├── processes/                   # 📁 Core automation & processing engine
│   ├── scraper.py               # Playwright browser automation & infinite scrolling
│   ├── parser.py                # DOM extraction logic for detail panels
│   └── storage.py               # Runtime CSV file generator & duplicate validator
│
├── leads/                       # 📁 Generated output folder (hierarchical CSVs)
│
├── venv/                        # Python virtual environment
├── main.py                      # CLI entry point & asynchronous orchestrator
└── requirements.txt             # Project dependencies



✨ Key Features
Playwright Asynchronous Engine: Fast and reliable browser automation.

Modular Design: Clean separation of configuration (config/), core execution logic (processes/), and data storage (data/ & leads/).

Anti-Bot & Anti-Duplicate Measures: Handles infinite scrolling, human-like delays, and skips duplicate leads using tracking ledgers.

Smart Inactivity Timeout: Automatically concludes searches and saves files if no new leads load within a specified timeframe.


Here is the complete, step-by-step process to download your structured Google Maps scraper project from GitHub and run it locally on your computer using Visual Studio Code (VS Code).

Step 1: Download or Clone the Project from GitHub
You can get your code onto your computer using one of two methods:

Method A: Using Git (Recommended if Git is installed)

Open your terminal or command prompt.

Run the clone command using your repository URL:

Bash
git clone <your-repository-url>
Navigate into the downloaded folder:

Bash
cd google-maps-scrapper
Method B: Downloading as a ZIP File

Go to your repository page on github.com.

Click the green Code button near the top right.

Select Download ZIP.

Extract the ZIP file and place the resulting google-maps-scrapper folder in your preferred workspace directory on your computer.

Step 2: Open the Project Folder in VS Code
Open Visual Studio Code on your computer.

Click on File in the top menu, then select Open Folder... (or press Ctrl + K then Ctrl + O on Windows / Cmd + O on Mac).

Navigate to and select your google-maps-scrapper folder, then click Select Folder.

Look at the Explorer sidebar on the left. You should see your exact project structure:

Plaintext
google-maps-scrapper/
├── config/          (contains config.py)
├── data/            (contains businesses.json, locations.json, etc.)
├── processes/       (contains scraper.py, parser.py, storage.py)
├── main.py
└── requirements.txt
Step 3: Recreate Your Virtual Environment (venv)
💡 Important Note: As a best practice, the local venv folder is excluded from GitHub because it contains heavy system binaries. You need to recreate your local sandbox.

Open the built-in terminal in VS Code by clicking Terminal -> New Terminal (or pressing Ctrl + ~).

Create a fresh virtual environment by running:

Windows:

Bash
python -m venv venv
macOS / Linux:

Bash
python3 -m venv venv
Activate the virtual environment:

Windows (PowerShell):

PowerShell
venv\Scripts\Activate.ps1
(Note: If you encounter a script execution policy error on PowerShell, run Set-ExecutionPolicy Unrestricted -Scope Process first, then run the activation command again).

Windows (Command Prompt):

DOS
venv\Scripts\activate.bat
macOS / Linux:

Bash
source venv/bin/activate
Confirmation: You will know it worked when (venv) appears at the very beginning of your terminal prompt line.

Step 4: Install Dependencies & Playwright Browsers
With your virtual environment active, install all required project packages and download the browser drivers:

Bash
pip install -r requirements.txt
playwright install

Step 5: Select Your Python Interpreter in VS Code
To ensure VS Code's editor (syntax highlighting, autocomplete, and linting) maps correctly to your newly created virtual environment:

Open the VS Code Command Palette using Ctrl + Shift + P (or Cmd + Shift + P on Mac).

Type and select: Python: Select Interpreter.

Choose the Python interpreter path that points to your virtual environment folder (it will look like: ./venv/Scripts/python.exe on Windows or ./venv/bin/python on Mac/Linux).

Step 6: Run Your Project (main.py)
Everything is now fully wired up and ready to execute!

In your active terminal (with (venv) visible), run your main orchestration file:

Bash
python main.py
The script will read your configurations from the config/ and data/ directories, initialize the Playwright automation engine inside the processes/ module, and output your scraped leads successfully!
