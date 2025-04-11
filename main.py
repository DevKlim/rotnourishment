import os
import argparse
import logging
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai # Use Google AI library
from gtts import gTTS
# Removed OpenAI import

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

OUTPUT_DIR = Path("output")
ASSETS_DIR = Path("assets")
DEFAULT_BACKGROUND = ASSETS_DIR / "background.png"
VIDEO_WIDTH = 720
VIDEO_HEIGHT = 1280

# Supported models (using Google Generative AI library)
SUPPORTED_MODELS = ["gemini-2.0-flash"] # Add more if integrating other APIs/models later

# --- Helper Functions ---

def ensure_dir(directory: Path):
    """Creates directory if it doesn't exist."""
    directory.mkdir(parents=True, exist_ok=True)

def read_note(filepath: Path) -> str:
    """Reads content from a markdown file."""
    logging.info(f"Reading note: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    return parts[2].strip()
            return content.strip()
    except FileNotFoundError:
        logging.error(f"Error: Input file not found at {filepath}")
        raise
    except Exception as e:
        logging.error(f"Error reading file {filepath}: {e}")
        raise

# --- LLM Integration (Google AI) ---
def generate_script_google_ai(note_content: str, model_name: str) -> str:
    """Generates a 'brainrot' style script using the specified Google AI model."""
    if model_name not in SUPPORTED_MODELS:
        raise ValueError(f"Model '{model_name}' is not supported by this script's current setup.")

    logging.info(f"Generating script via Google AI model: {model_name}...")

    # Configure generation settings (optional, adjust as needed)
    generation_config = {
        "temperature": 0.8,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 300, # Gemini uses token count differently
    }

    # Configure safety settings (adjust level if needed, e.g., BLOCK_MEDIUM_AND_ABOVE)
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]

    prompt = f"""
    Transform the following note content into a short, chaotic, slightly unhinged, but still educational script for a 30-60 second TikTok/YouTube Short video. Use a 'brainrot' style: fast-paced, maybe hyperbolic, meme-adjacent humor, but ensure the core concepts from the note are mentioned. Keep it concise and engaging for a short-form video format.

    Note Content:
    ---
    {note_content}
    ---

    Generated Script:
    """

    try:
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        response = model.generate_content(prompt)

        # Check for valid response text, handle potential blocks
        if not response.parts:
            block_reason = "Unknown"
            if response.prompt_feedback and response.prompt_feedback.block_reason:
                 block_reason = response.prompt_feedback.block_reason.name
            # Check candidates as well
            elif response.candidates and response.candidates[0].finish_reason != 'STOP':
                 block_reason = f"Candidate Finish Reason: {response.candidates[0].finish_reason.name}"

            logging.error(f"Google AI generation failed or was blocked. Reason: {block_reason}")
            if response.candidates and response.candidates[0].safety_ratings:
                 logging.error(f"Safety Ratings: {response.candidates[0].safety_ratings}")

            raise ValueError(f"Script generation failed. The response was empty or blocked (Reason: {block_reason}). Try adjusting safety settings or the note content.")

        script = response.text
        logging.info(f"Generated script: {script[:100]}...")
        return script

    except Exception as e:
        logging.error(f"Error calling Google AI API ({model_name}): {e}")
        # You might want to catch specific Google API exceptions here later
        raise


# --- TTS and Video Functions (remain the same) ---

def synthesize_audio(script_text: str, output_path: Path) -> Path:
    """Synthesizes audio from text using gTTS."""
    logging.info(f"Synthesizing audio to {output_path} using gTTS...")
    try:
        tts = gTTS(text=script_text, lang='en', slow=False)
        tts.save(str(output_path))
        logging.info("Audio synthesis complete.")
        return output_path
    except Exception as e:
        logging.error(f"Error during audio synthesis: {e}")
        raise

def get_audio_duration(audio_path: Path) -> float:
    """Gets audio duration using ffprobe."""
    cmd = [
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        duration = float(result.stdout.strip())
        logging.info(f"Audio duration: {duration:.2f} seconds")
        return duration
    except FileNotFoundError:
        logging.error("ffprobe command not found. Is ffmpeg installed and in PATH?")
        raise
    except subprocess.CalledProcessError as e:
        logging.error(f"ffprobe failed: {e.stderr}")
        raise
    except ValueError:
        logging.error(f"Could not parse ffprobe duration output: {result.stdout}")
        raise

def create_video_ffmpeg(audio_path: Path, video_duration: float, note_title: str, background_path: Path, output_path: Path):
    """Creates video using direct ffmpeg commands."""
    logging.info(f"Creating video with ffmpeg: {output_path}")
    if not background_path.exists():
        raise FileNotFoundError(f"Background image not found: {background_path}")

    font_name = 'Arial-Bold' # Adjust if needed, see previous comments
    safe_title = note_title.replace("'", "\\'").replace(":", "\\:").replace(",", "\\,")

    filtergraph = (
        f"[0:v]scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=decrease,"
        f"pad={VIDEO_WIDTH}:{VIDEO_HEIGHT}:(ow-iw)/2:(oh-ih)/2,"
        f"format=yuv420p[bg];"
        f"[bg]drawtext=font='{font_name}':"
        f"text='{safe_title}':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=h*0.1:"
        f"box=1:boxcolor=black@0.5:boxborderw=5[outv]"
    )
    cmd = [
        'ffmpeg', '-loop', '1', '-i', str(background_path), '-i', str(audio_path),
        '-filter_complex', filtergraph, '-map', '[outv]', '-map', '1:a',
        '-c:v', 'libx264', '-preset', 'fast', '-tune', 'stillimage',
        '-c:a', 'aac', '-b:a', '192k', '-shortest', '-t', str(video_duration),
        '-y', str(output_path)
    ]
    logging.info(f"Executing ffmpeg command: {' '.join(cmd)}")
    try:
        process = subprocess.run(cmd, capture_output=True, text=True, check=True)
        logging.info("ffmpeg stdout:\n" + process.stdout)
        logging.info("ffmpeg stderr:\n" + process.stderr)
        logging.info(f"Video saved successfully to {output_path}")
    except FileNotFoundError:
        logging.error("ffmpeg command not found. Is ffmpeg installed and in PATH?")
        raise
    except subprocess.CalledProcessError as e:
        logging.error(f"ffmpeg failed with exit code {e.returncode}")
        logging.error("ffmpeg stdout:\n" + e.stdout)
        logging.error("ffmpeg stderr:\n" + e.stderr)
        raise
    finally:
        if audio_path.exists():
            try: os.remove(audio_path); logging.info(f"Cleaned up temp audio: {audio_path}")
            except OSError as e: logging.warning(f"Could not remove temp audio {audio_path}: {e}")


# --- Main Execution ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a 'brainrot' video from an Obsidian note using Google AI and ffmpeg.")
    parser.add_argument("note_file", help="Path to the input Obsidian Markdown file.")
    parser.add_argument("-o", "--output", help="Optional: Output video file name (without extension). Defaults to note name.")
    parser.add_argument("-bg", "--background", default=str(DEFAULT_BACKGROUND), help=f"Optional: Path to background image. Defaults to {DEFAULT_BACKGROUND}")
    parser.add_argument(
        "-m", "--model",
        default="gemini-2.0-flash",
        choices=SUPPORTED_MODELS, # Use the defined list
        help=f"Generative model to use (Google AI). Supported: {', '.join(SUPPORTED_MODELS)}"
    )

    args = parser.parse_args()

    input_path = Path(args.note_file)
    background_path = Path(args.background)
    selected_model = args.model

    note_basename = input_path.stem
    output_filename = args.output if args.output else note_basename
    video_output_path = OUTPUT_DIR / f"{output_filename}.mp4"
    temp_audio_path = OUTPUT_DIR / f"{output_filename}_temp.mp3"

    ensure_dir(OUTPUT_DIR)

    # --- Pipeline ---
    try:
        # 1. Configure Google AI Client
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env file or environment variables.")
        genai.configure(api_key=google_api_key)
        logging.info("Google AI Client configured.")

        # 2. Read Note
        note_content = read_note(input_path)
        if not note_content:
            raise ValueError("Note content is empty or could not be read properly.")

        # 3. Generate Script (using selected Google AI model)
        script_text = generate_script_google_ai(note_content, selected_model)

        # 4. Synthesize Audio
        synthesize_audio(script_text, temp_audio_path)

        # 5. Get Audio Duration
        duration = get_audio_duration(temp_audio_path)

        # 6. Create Video
        create_video_ffmpeg(temp_audio_path, duration, note_basename, background_path, video_output_path)

        logging.info("--- Process Completed Successfully ---")

    except FileNotFoundError as fnf_error:
        logging.error(f"File Not Found Error: {fnf_error}. Check paths and ffmpeg installation.")
    except ValueError as ve:
        logging.error(f"Configuration or Value Error: {ve}. Exiting.")
    except subprocess.CalledProcessError:
        logging.error("ffmpeg/ffprobe command failed. Check logs above for details.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        logging.info("--- Process Failed ---")