import os
from google.cloud import texttospeech_v1
from google.cloud.texttospeech_v1.types import SynthesizeLongAudioRequest
from google.cloud.texttospeech_v1.types import SynthesisInput
from google.cloud.texttospeech_v1.types import VoiceSelectionParams
from google.cloud.texttospeech_v1.types import AudioConfig

''' Change lines at bottom of this script to text path destination, and google cloud file path
    Simply run "python long_text_to_audio_gcp.py" from this folder ensuring 
    export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your_service_account.json" is run from bash,
    "source venv/bin/activate" is run from bash
'''
def synthesize_long_audio(
    text_file_path,
    gcs_audio_output_uri,
    language_code="en-US",
    voice_name=None,
    audio_encoding=texttospeech_v1.AudioEncoding.LINEAR16
):
    """
    Synthesize long text into an audio file using Google Cloud's Long Audio Synthesis.
    :param text_file_path: Local path to the text file you want to convert.
    :param gcs_audio_output_uri: "gs://BUCKET_NAME/FOLDER/filename.mp3"
    :param language_code: e.g. "en-US"
    :param voice_name: e.g. "en-US-Wavenet-D" (optional)
    :param audio_encoding: e.g. texttospeech_v1.AudioEncoding.MP3
    """

    # 1) Read text from local file
    with open(text_file_path, 'r', encoding='utf-8') as f:
        text_content = f.read()

    # 2) Create a client specifically for long audio
    client = texttospeech_v1.TextToSpeechLongAudioSynthesizeClient()

    # 3) Build the voice request
    voice = VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,  # Optional: use a specific Wavenet voice. If None, TTS picks a default.
        ssml_gender=texttospeech_v1.SsmlVoiceGender.NEUTRAL
    )

    # 4) Specify the audio config
    audio_config = AudioConfig(
        audio_encoding=audio_encoding
    )

    # 5) Prepare the input text (up to ~300K characters inline)
    synthesis_input = SynthesisInput(text=text_content)

    # 6) Specify the GCS destination
    # The request will store the synthesized audio into this GCS location
    

    # 7) Assemble the request
    request = SynthesizeLongAudioRequest(
        # Change the default project id below
        parent="projects/YOUR-PROJECT-ID/locations/global", 
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
        output_gcs_uri=gcs_audio_output_uri,
    )

    # 8) Start the long-running operation
    operation = client.synthesize_long_audio(request=request)

    print("Long audio synthesis in progress...")
    # 9) Wait for the operation to complete
    response = operation.result()  # This can take a while for large text

    print("Long audio synthesis complete!")
    print(f"Audio file saved to: {gcs_audio_output_uri}")

if __name__ == "__main__":
    # Replace two lines below this one!!!!
    text_file = "FILE-NAME.txt"
    # Provide a valid GCS URI where the output audio should be stored
    gcs_audio_output = "gs://GOOGLE-CLOUD-BUCKET/FILE-NAME.wav"

    synthesize_long_audio(
        text_file_path=text_file,
        gcs_audio_output_uri=gcs_audio_output,
        language_code="en-US",
        voice_name="en-US-Wavenet-D"
    )
