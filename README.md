# Project Overview
This is a **YouTube Video Downloader** built using **Flask** and **yt-dlp**, designed for downloading YouTube videos and audio in various formats. The project provides a Simple web interface built using **Bootstrap**. Users can easily download videos or audio with an option to choose from the best available formats.

## Features
- Download YouTube videos in multiple resolutions.
- Download audio-only formats.
- Separate sections for video and audio formats.
- Automatically shows the best formats.
- User-friendly web interface built with Bootstrap for a Simple design.
- Built with Python Flask for the backend and Bootstrap for the frontend.

## Requirements

To run the project, make sure you have the following installed:
- Python 3.8 or higher
- pip (Python package manager)

## Python Libraries:
Install the required Python packages using the following command:
```bash
pip install -r requirements.txt
```
```requirements.txt``` contains:
- Flask
- yt-dlp

## Installation and Setup
### Clone the Repository
```bash
git clone https://github.com/AKRASH-Nadeem/YoutubeVideoDownloader.git
cd YoutubeVideoDownloader
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Application
```bash
python app.py
```

### Access the Application
Open your browser and navigate to:


```bash
http://127.0.0.1:5000
```

## How to Use
1. Paste YouTube Link: Copy a video link from YouTube and paste it into the input field on the webpage.
2. Choose Format: The available formats are displayed in two sections:
    - Audio Only: Lists the best two audio-only formats.
    - Video Options: Lists the best two video-only formats and normal video options.

3. Download: Click the download button to start downloading your selected format.

## Folder Structure
```bash
YoutubeVideoDownloader/
│
├── app.py                 # Main Flask application file
├── templates/
│   ├── index.html         # Frontend HTML with Bootstrap
├── requirements.txt       # Python dependencies
├── README.md              # ReadMe file
```
## Features in Detail
### Backend
- **Flask**: Serves the web application and handles the logic for downloading videos using yt-dlp.
- **yt-dlp**: A powerful command-line program to download videos and extract audio from YouTube and other video platforms.
### Frontend
- **Bootstrap**: Used to create an elegant and responsive web page.

# License

This project is licensed under the MIT License. Feel free to modify and use it in your own projects.

# Contact

For any queries or feedback, feel free to reach out:
- Name: Akrash Nadeem
- Email: akrashnadeemprogrammer@gmail.com
- GitHub: AKRASH-Nadeem

### Note:

This project is for **educational purposes only**. Please ensure you comply with YouTube’s Terms of Service when using this application.