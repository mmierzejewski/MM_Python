import os
import re
from pytubefix import YouTube
from tqdm import tqdm
import subprocess

def sanitize_filename(filename):
    # Replace invalid characters with underscores and normalize spaces
    filename = re.sub(r'[<>:"/\\|?*\n\r]', '_', filename)
    filename = re.sub(r'\s+', '_', filename.strip())
    return filename

def download_youtube_video(url, output_path):
    try:
        # Normalize and create output directory
        output_path = os.path.normpath(output_path)
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Create YouTube object
        yt = YouTube(url)

        # Get best video and audio streams
        video_stream = yt.streams.filter(file_extension='mp4', only_video=True).order_by('resolution').desc().first()
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

        if not video_stream or not audio_stream:
            print("Could not find suitable video or audio streams.")
            return

        # Sanitize title for filenames
        sanitized_title = sanitize_filename(yt.title)

        # Download video
        print(f"\nDownloading video: {yt.title} in resolution {video_stream.resolution}")
        video_file_path = os.path.join(output_path, f"{sanitized_title}_video.mp4")
        video_file_size = video_stream.filesize

        video_progress_bar = tqdm(total=video_file_size, unit='B', unit_scale=True, desc="Video Download", ascii=True)
        audio_progress_bar = tqdm(total=audio_stream.filesize, unit='B', unit_scale=True, desc="Audio Download", ascii=True)

        def on_progress(stream, chunk, bytes_remaining):
            if stream == video_stream:
                video_progress_bar.update(len(chunk))
            else:
                audio_progress_bar.update(len(chunk))

        yt.register_on_progress_callback(on_progress)
        video_stream.download(output_path=output_path, filename=f"{sanitized_title}_video.mp4")

        # Download audio
        print(f"\nDownloading audio: {yt.title} with bitrate {audio_stream.abr}")
        audio_file_path = os.path.join(output_path, f"{sanitized_title}_audio.mp4")
        audio_progress_bar.reset()  # Reset for audio
        audio_stream.download(output_path=output_path, filename=f"{sanitized_title}_audio.mp4")

        # Verify files exist
        if not os.path.exists(video_file_path) or not os.path.exists(audio_file_path):
            print(f"Error: Video file ({video_file_path}) or audio file ({audio_file_path}) not found.")
            return

        # Merge video and audio
        merged_file_path = os.path.join(output_path, f"{sanitized_title}.mp4")
        print(f"\nMerging video and audio into: {merged_file_path}")
        result = subprocess.run([
            'ffmpeg', '-i', video_file_path, '-i', audio_file_path, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', merged_file_path
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"FFmpeg merge failed: {result.stderr}")
            return

        # Clean up temporary files
        os.remove(video_file_path)
        os.remove(audio_file_path)

        print(f"Successfully downloaded and merged as: {merged_file_path}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if "HTTP Error 400" in str(e):
            print("Possible causes of HTTP 400 error:")
            print("- Incorrect or unavailable video link.")
            print("- Video is restricted (e.g., private, regionally blocked).")
            print("- The pytubefix library version is outdated. Update: pip install --upgrade pytubefix")
            print("- YouTube changed the page structure, try using the latest version of pytubefix.")
        print("Check the link and try again.")

def main():
    url = input("Enter the YouTube video link: ")
    output_path = input("Enter the directory path to save the video (e.g., /Users/yourname/Videos): ") or os.getcwd()
    download_youtube_video(url, output_path)

if __name__ == "__main__":
    main()