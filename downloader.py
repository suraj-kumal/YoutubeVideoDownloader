import yt_dlp
import re


# get the video information
def video_info(url):

    # extract video information without downloading

    try:

        # creating an instance
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)

            # Get video title from the info dictionary
            title = info.get("title", "Unknown Title")

            # Get all available formats
            formats = info.get("formats", [])

            resolutions = []

            for fmt in formats:
                height = fmt.get("height")
                if height is not None and isinstance(height, int):
                    resolutions.append(f"{height}p")

            # Remove duplicates and sort all resolutions
            resolutions = sorted(set(resolutions), key=lambda x: int(x[:-1]))

            # Filter out resolutions 360p and below
            resolution_list = [res for res in resolutions if int(res[:-1]) >= 360]

            return title, resolution_list

    except Exception as e:
        return "invalid url or video doesnt exists", []


def download_video(url, resolution, download_path, title, progress_var):
    format_string_map = {
        "360p": "bestvideo[height<=360]+bestaudio[ext=m4a]/best",
        "480p": "bestvideo[height<=480]+bestaudio[ext=m4a]/best",
        "720p": "bestvideo[height<=720]+bestaudio[ext=m4a]/best",
        "1080p": "bestvideo[height<=1080]+bestaudio[ext=m4a]/best",
        "1440p": "bestvideo[height<=1440]+bestaudio[ext=m4a]/best",
        "2160p": "bestvideo[height<=2160]+bestaudio[ext=m4a]/best",
    }

    format_string = format_string_map.get(
        resolution, "bestvideo+bestaudio[ext=m4a]/best"
    )

    ydl_output = {
        "format": format_string,
        "outtmpl": f"{download_path}/{title}.%(ext)s",
        "merge_output_format": "mp4",
        "progress_hooks": [lambda d: progress_var.set(display_progress(d))],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_output) as ydl:
            ydl.download([url])
    except yt_dlp.utils.DownloadError as e:
        return f"Failed to download video: {e}"


def display_progress(d):
    if d["status"] == "downloading":
        
        # Strip ANSI color codes
        progress = re.sub(r"\x1b\[[0-9;]*m", "", d["_percent_str"])
        eta = re.sub(r"\x1b\[[0-9;]*m", "", d["_eta_str"])


        return f"Downloading: {progress} complete, {eta} remaining"
    elif d["status"] == "finished":
        return "Download Completed"
    return ""
