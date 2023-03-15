VORPAL: Versatile Online Repository for Playback and Analysis of Libraries

VORPAL is a music streaming server designed to serve as a personal music library for web and mobile applications.
Features

    RESTful API for managing and streaming audio files
    Support for various audio formats
    Metadata extraction and management
    Audio playback with a built-in web player
    Real-time audio spectrum visualization
    Easy integration with web and mobile applications

Endpoints

VORPAL provides a comprehensive set of API endpoints to manage and stream audio files:

    GET / - Display available API endpoints
    GET /api/media - Retrieve all media files
    GET /api/media/search - Search for media files based on metadata
    POST /api/media - Add a new media file
    PUT /api/media/:media_id - Update an existing media file
    DELETE /api/media/:media_id - Delete a media file
    GET /api/media/:media_id - Retrieve a specific media file
    GET /api/media/:media_id/stream - Stream a specific media file
    GET /api/media/format/:format_name - Retrieve media files of a specific format
    GET /api/media/metadata/:metadata_key/:metadata_value - Retrieve media files with specific metadata

Setup
Requirements

    Python 3.7 or higher
    Flask web framework
    SQLAlchemy ORM
    FFmpeg (optional, for transcoding and manifest generation)

Installation

    Clone the repository and navigate to the project directory:

bash

git clone https://github.com/your-github-username/vorpal.git
cd vorpal

    Create a virtual environment and activate it:

bash

python -m venv venv
source venv/bin/activate

    Install the required dependencies:

pip install -r requirements.txt

    Run the server:

css

python main.py

    Access the web player in your browser at http://localhost:5000/.

Acknowledgements

This project was created by The Creator with assistance from OpenAI's ChatGPT.
License

VORPAL is released under the MIT License. See LICENSE for more information.
