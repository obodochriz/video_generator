# Video Generator

A modular Python application for automatically generating YouTube-style videos from text topics using AI providers like OpenAI and Google Gemini.

## Description

This project generates complete videos by:
1. Creating a script based on a user-provided topic and duration
2. Parsing the script into scenes with narration and visual prompts
3. Generating voiceovers for each scene
4. Fetching stock videos or generating AI images for visuals
5. Combining everything into a final video with subtitles and thumbnail

The system supports multiple AI providers and intelligently blends stock footage with AI-generated content for cost-effective video production.

## Features

- **AI-Powered Scripting**: Generate video scripts using OpenAI GPT or Google Gemini
- **Modular Architecture**: Easily extensible with new AI providers and video components
- **Stock Video Integration**: Automatically fetch and use free stock videos from Pexels
- **AI Image Generation**: Fallback to AI-generated images when stock videos aren't available
- **Text-to-Speech**: Generate natural voiceovers for narration
- **Video Editing**: Professional video composition with cinematic effects (zoom, pan, fade)
- **Subtitle Generation**: Automatic SRT subtitle file creation
- **Thumbnail Generation**: AI-generated video thumbnails
- **YouTube Optimization**: Videos formatted for 1920x1080 (16:9) aspect ratio

## Installation

1. **Clone or navigate to the project directory**

2. **Install Python dependencies**:
   ```bash
   pip install openai google-generativeai moviepy pydantic-settings requests pillow
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   PEXELS_API_KEY=your_pexels_api_key_here
   ```

## Usage

Run the main script:

```bash
python main.py
```

You'll be prompted to enter:
- **Topic**: The subject of your video (e.g., "The History of Artificial Intelligence")
- **Duration**: Target video length in seconds (e.g., 60)
- **Model**: Choose "openai" or "gemini"

The script will generate:
- A video file named after the topic
- `subtitles.srt` for subtitles
- A thumbnail image

## Project Structure

```
video_generator/
├── main.py                 # Main entry point
├── config.py              # Configuration and API keys
├── README.md              # This file
├── subtitles.srt          # Generated subtitles
├── ai_providers/          # AI provider implementations
│   ├── base.py            # Abstract base class
│   ├── openai_provider.py # OpenAI GPT integration
│   └── gemini_provider.py # Google Gemini integration
└── video/                 # Video generation components
    ├── video_builder.py   # Main video composition
    ├── scene_parser.py    # Script parsing
    ├── tts_generator.py   # Text-to-speech
    ├── image_generator.py # AI image generation
    ├── stock_video_fetcher.py # Stock video fetching
    ├── subtitle_generator.py  # SRT file creation
    ├── thumbnail_generator.py # Thumbnail creation
    ├── music_mixer.py     # (Future) Background music
    └── utils.py           # Utility functions
```

## Configuration

The application uses Pydantic settings loaded from a `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API key
- `GEMINI_API_KEY`: Your Google Gemini API key
- `PEXELS_API_KEY`: Your Pexels API key for stock videos

## Dependencies

- `openai`: OpenAI API client
- `google-generativeai`: Google Gemini API client
- `moviepy`: Video editing and composition
- `pydantic-settings`: Configuration management
- `requests`: HTTP requests for stock video fetching
- `pillow`: Image processing

## Contributing

This is a modular project designed for easy extension. To add a new AI provider:

1. Create a new class inheriting from `AIProvider` in `ai_providers/`
2. Implement the `generate_script` method
3. Update `main.py` to include the new provider

## License

This project is owned and maintained by Obodo Christopher