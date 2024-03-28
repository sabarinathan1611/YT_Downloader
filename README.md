# YouTube Video Downloader

This Flask application allows users to download YouTube videos in various resolutions. It utilizes the Pytube library for fetching video streams and MoviePy for handling scenarios where the selected stream lacks audio. The application provides endpoints for initiating video downloads and serving downloaded files.

## Features

- Download YouTube videos by specifying the video URL and desired resolution.
- Automatically handles scenarios where the selected video stream lacks audio.
- Supports serving downloaded files through a Flask endpoint.
- Robust error handling to address connectivity issues and ensure smooth performance.

## Requirements

- Python 3.x
- Flask
- Pytube


## Installation

1. Clone this repository:

    ```
    git clone https://github.com/sabarinathan1611/YT_Downloader.git
    ```

2. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

3. Run the Flask application:

    ```
    python app.py
    ```

## Usage

1. Access the application through a web browser or API client.
2. Provide the YouTube video URL and desired resolution.
3. Initiate the download process.
4. Once the download is complete, the file will be available for download or streaming.

## API Endpoints

- `POST /download`: Initiates the download process by providing the video URL and resolution in JSON format.
- `GET /download/<filename>`: Serves the downloaded file with the specified filename.

## Contributors

- [Sabarinathan](https://github.com/sabarinathan1611)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
