import os
import glob
from flask import Flask, render_template, request, send_file
import yt_dlp
import datetime

app = Flask(__name__)

# Define download directory
DOWNLOAD_DIR = "downloads"

# Home page
@app.route("/", methods=["GET", "POST"])
def index():
    # Handle Post request: get information of the video
    if request.method == "POST":
        video_url = request.form.get("url") # get URL of the video from Request (Http)
        if not video_url:
            # return template with error if no url is given
            return render_template("index.html", error="Please provide a valid YouTube URL.")

        try:
            ydl_opts = { # Options for yt-dlp
                "quiet": True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl: # Create YoutubeDownloder Object with given options (ydl_opts)
                info = ydl.extract_info(video_url, download=False) # get information fo the video

            formats = info.get("formats", []) # get video formats(audio and video)
            thumbnail_url = info.get("thumbnail", "") # get thumbnail of the video
            video_title = info.get("title", "Unknown Title") # get title of the video
            
            # Filter and group video formats
            video_formats = [f for f in formats if f.get("vcodec") != "none"]
            grouped_formats = {}

            for f in video_formats:
                resolution = f"{f.get('height', 0)}p"
                if resolution not in grouped_formats:
                    grouped_formats[resolution] = []
                grouped_formats[resolution].append(f)
            # For each resolution, sort by FPS and select up to 2 variants
            selected_formats = []
            for resolution, variants in sorted(grouped_formats.items(), key=lambda x: int(x[0].replace("p", "")), reverse=True):
                seen_fps = set()
                variants_sorted = sorted(
                    [v for v in variants if (fps := int(v.get("fps"))) not in seen_fps and not seen_fps.add(fps)],
                    key=lambda x: int(x.get("fps", 0) or 0),
                    reverse=True
                )
                selected_formats.extend(variants_sorted[:2])  # Select up to 2 variants per resolution
                if len(selected_formats) >= 4:  # Stop once we have 4 formats
                    break

            # Limit to the best 4 formats
            selected_formats = selected_formats[:4]

            # Check and handle audio for video formats
            for fmt in selected_formats:
                if fmt.get("acodec") == "none":  # Video format without audio
                    best_audio = [f for f in formats if f.get("vcodec") == "none" and f.get("format_note") != "storyboard"][-1]
                    if best_audio:
                        # Combine video and audio formats using the + method
                        fmt["format_id"] = f"{fmt['format_id']}+{best_audio['format_id']}"

            # Extract audio formats (best 2 by bitrate)
            audio_formats = sorted(
                [f for f in formats if f.get("vcodec") == "none"],
                key=lambda x: x.get("abr", 0) or 0,
                reverse=True
            )[:2]

            # Return the html file with the video data
            return render_template(
                "index.html",
                url=video_url,
                video_title=video_title,
                thumbnail_url=thumbnail_url,
                audio_formats=audio_formats,
                video_formats=selected_formats,
            )
        except Exception as e:
            return render_template("index.html", error=f"Error fetching formats: {str(e)}")

    # Handle Get request: send html template
    return render_template("index.html")


@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")
    video_title = request.args.get("title")
    format_id = request.args.get("format_id")
    ext = request.args.get("ext") # extension of the video
    
    if not url or not format_id or not ext or not video_title:
        return "Invalid request", 400

    # Generate a unique filename using the current datetime
    datetime_filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_path = os.path.join("downloads", f"{datetime_filename}.{ext}")

    try:

        # Determine if the format is combined(format1+format2) or single
        is_single_format = "+" not in format_id

        # Options for yt-dlp download
        ydl_opts = {
            "format": format_id, # format to download
            "outtmpl": output_path, # file path where we want to download
        }

        # For video+audio, ensure MP4 as output format
        if not is_single_format:
            ydl_opts["merge_output_format"] = "mp4"

        # Download the file
        with yt_dlp.YoutubeDL(ydl_opts) as ydl: # Create the Youtube Downloader Object for downloading
            ydl.download([url])
        # Use the video title as the file name for the user
        user_filename = f"{video_title}.{ext}"

        # Send the file to the user
        return send_file(output_path, as_attachment=True, download_name=user_filename)

    except Exception as e:
        return f"Error during download: {str(e)}", 500

# Clean up temp files
@app.teardown_request
def cleanup(exception=None):
    """Cleanup temporary files after each request."""
    if os.path.exists(DOWNLOAD_DIR):
        # Remove all temporary files in the download directory
        for temp_file in glob.glob(os.path.join(DOWNLOAD_DIR, "*")):
            try:
                os.remove(temp_file)
            except Exception as e:
                print(f"Error cleaning up file {temp_file}: {str(e)}")


if __name__ == "__main__":
    # Ensure download directory exists
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    app.run(debug=True)
