# smol notebook lm

Generates an AI news podcast (and optional video) from raw text. GPT-4o writes a 3-host dialogue, which is then converted to speech using **three TTS providers** — one per host — and stitched into a single audio file. Ensure `rawtext.md` is updated, all environment keys are loaded, and outputs are available in `.mp3`, `.txt`, and `.log` formats.

You can see sample output here: https://github.com/smol-ai/temp

### Text-to-Speech providers

Each speaker is routed to a different TTS provider (see `voice_config` in `main.py`):

| Speaker | Provider | Endpoint |
|---------|----------|----------|
| Host (Charlie) | **ElevenLabs** | `POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream` |
| Karan | **Cartesia** | `POST https://api.cartesia.ai/tts/bytes` |
| Sarah | **60db** | `POST https://api.60db.ai/tts-synthesize` |

All three return MP3 (60db is base64-decoded from JSON), and clip durations are measured with `pydub` so caption timestamps stay consistent across providers.


## requirements

- make sure ffmpeg is installed
- `brew install imagemagick`

### Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables:**
   ```bash
   export ELEVENLABS_API_KEY=your_api_key
   export OPENAI_API_KEY=your_api_key
   export CARTESIA_API_KEY=your_api_key # note that this thing generates a lot of tokens. we used up 52k cahracters just developing this.
   export SIXTYDB_API_KEY=your_api_key # 60db (https://api.60db.ai) — used for Sarah's voice
   ```

3. **Update `rawtext.md`:**
   - Add or modify the text you want to convert to speech.

4. **Set Sarah's 60db voice ID:**
   - List the voices on your 60db account (calls `GET https://api.60db.ai/myvoices`):
     ```bash
     python list_60db_voices.py
     ```
   - Copy a `voice_id` from the output into `main.py` → `voice_sarah_id`.

5. **Run the Script:**
   ```bash
   python main.py
   ```

### Optional Video Generation

To generate a video from the audio and transcript, you can use the `video.py` script. This script uses the MoviePy library to combine the audio and image, and the OpenAI library to generate a default image using DALL·E.

#### Requirements

- Make sure you have the `moviepy` and `openai` libraries installed. You can install them using pip:
  ```bash
  pip install moviepy openai
  ```

#### Setup

1. **Set Environment Variables:**
   ```bash
   export OPENAI_API_KEY=your_api_key
   ```

2. **Run the Script:**
   ```bash
   python video.py
   ```

#### Outputs

- **Video:** `final_video.mp4` file

### Notes

- The `video.py` script assumes that the `combined_dialogue.mp3` and `dialogue_transcript.txt` files are present in the same directory.
- The script generates a default image using DALL·E and resizes it to 1080x1080 pixels.
- The script combines the audio and image to create a video, and adds captions using the transcript.
- The final video is saved as `final_video.mp4` in the same directory.



### Outputs

- **Audio:** `.mp3` files
- **Transcript:** `.txt` files
- **Logs:** `.log` files

### 60db integration (what's new)

- **Sarah's voice now uses 60db** via `POST /tts-synthesize` (base64 MP3 decoded to disk). Host stays on ElevenLabs, Karan on Cartesia.
- `text_to_speech_file()` switched from a `use_cartesia` flag to a `provider` selector (`elevenlabs` / `cartesia` / `60db`), with routing driven by a `voice_config` dict in `main()`.
- New `SIXTYDB_API_KEY` env var (added to `.env` and validation).
- New `list_60db_voices.py` helper to fetch your voice IDs (`GET /myvoices`).

> **Reminder:** 60db's TTS response carries no generation/history ID, so Sarah's lines are synthesized independently — there's no cross-line voice continuity (same as Cartesia for Karan). This is expected.

### Examples

- [Sample MP3](examples/combined_dialogue.mp3)
- [Transcript](examples/dialogue_transcript.txt)
```
