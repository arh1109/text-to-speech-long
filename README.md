This project demonstrates how to convert large text files (under 500k characters) into audio (WAV) using **Google Cloud Text-to-Speech’s Long Audio Synthesis**. The resulting audio is written to a Google Cloud Storage bucket.

## Table of Contents

1. [Prerequisites](#prerequisites)  
2. [Set Up Google Cloud Resources](#set-up-google-cloud-resources)  
3. [Clone This Repository](#clone-this-repository)  
4. [Create a Python Virtual Environment](#create-a-python-virtual-environment)  
5. [Install Dependencies](#install-dependencies)  
6. [Set Up Your GCP Credentials](#set-up-your-gcp-credentials)  
7. [Usage](#usage)  
8. [Notes](#notes)

---

## Prerequisites

- A **Google Cloud** account ([sign up here](https://cloud.google.com/) if you don’t have one).
- A **billing-enabled** Google Cloud project.
- Python **3.7+** installed on your system.
- (Optional) [Git](https://git-scm.com/) if you want to clone via command line.

---

## Set Up Google Cloud Resources

1. **Create or Select a Google Cloud Project**  
   - Go to your [GCP Console](https://console.cloud.google.com/).  
   - Make sure **billing** is enabled for your project. (This is required for TTS long-audio.)

2. **Enable Text-to-Speech API**  
   - In the [GCP Console](https://console.cloud.google.com/marketplace/product/google/texttospeech.googleapis.com), click **Enable** if it’s not already.

3. **Create a Service Account**  
   - Navigate to **IAM & Admin** → **Service Accounts**.  
   - Click **Create Service Account**, give it a name (e.g. `tts-long-audio-sa`).  
   - Assign a role like **“Text-to-Speech Admin”**.  
     - If you also need to read/write from Cloud Storage, add **“Storage Object Admin”** (or more restricted roles as needed).

4. **Create Service Account Key**  
   - Under your service account, go to **Manage Keys** → **Add Key** → **Create new key** → **JSON**.  
   - A JSON key file will be downloaded (e.g. `tts-service-account.json`).

5. **Create a Cloud Storage Bucket**  
   - In the [Cloud Console](https://console.cloud.google.com/storage/browser), click **Create Bucket**.  
   - Choose a unique name, e.g. `my-tts-bucket`, and configure the region/permissions as desired.

---

## Clone This Repository

```bash
git clone https://github.com/YourUsername/your-long-tts-project.git
cd your-long-tts-project
```

## Create a Python Virtual Environment

It's best practice to isolate dependencies in a virtual environment:
# Windows (Command Prompt)

```bat
python -m venv venv
venv\Scripts\activate
```

# Windows (Powershell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

# macOS / Linux
```bash
python -m venv venv
source venv/bin/activate
```
You should see (venv) in your terminal prompt indicating the environment is active.

---

## Install Dependencies

Insided the activated virtual environment:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Or, if you don't have a requirement.txt, install manually:

```bash
pip install google-cloud-texttospeech==2.14.0 google-cloud-storage
```
(I couldn't get it to work with google-cloud-texttospeech==2.25)

---

## Set Up Your GCP Credentials

1. Move or copy your service account JSON file (e.g., tts-service-account.json) into a secure location (not committed to Git!).

2. Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to point to it:

# Windows (Command Prompt):
```bat
set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\tts-service-account.json
```

# Windows (PowerShell):
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\tts-service-account.json"
```

# macOS / Linux:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/tts-service-account.json"
```

---

## Usage

1. Place your input text file (e.g., Chromatography.txt) in the project folder.

2. Edit the Python script (e.g. long_text_to_audio_gcp.py) if needed:
  - Update PROJECT_ID (if it’s hardcoded)
  - Update BUCKET_NAME (the GCS bucket where you want to store the output)
  - Ensure the audio encoding is LINEAR16 (since MP3 is not currently supported for long-audio).

3. Run the script:
  ```bash
  python long_text_to_audio_gcp.py
  ```

4. The script will:
  - Read the text from Chromatography.txt
  - Send a long-audio synthesis request
  - Write the resulting .wav (LINEAR16) file to your GCS bucket

---

## Notes

  - Billing must be active for your GCP project or the API call will fail.
  - The Long Audio Synthesis API only supports LINEAR16 encoding at this time. You can convert WAV to MP3 locally using a tool like ffmpeg.
  - If your text is over 300K characters, you must supply it via a GCS URI instead of inline text. See Long Audio Synthesis docs for more details.
  - For troubleshooting:
    - Ensure your service account has Text-to-Speech and Storage permissions.
    - Verify the correct credentials file is referenced by GOOGLE_APPLICATION_CREDENTIALS.
    - Confirm you’re using the correct project ID and bucket name.

