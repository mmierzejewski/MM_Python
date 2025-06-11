from pytubefix import YouTube
import os
from tqdm import tqdm
import subprocess

def download_youtube_video(url, output_path):
    try:
        # Check if the directory exists, if not - try to create it
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Create a YouTube object from the given link
        yt = YouTube(url)

        # Get the best video stream (highest resolution)
        video_stream = yt.streams.filter(file_extension='mp4', only_video=True).order_by('resolution').desc().first()

        # Get the best audio stream (highest bitrate)
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

        if not video_stream or not audio_stream:
            print("Could not find suitable video or audio streams.")
            return

        # Download video with progress bar
        print(f"\nDownloading video: {yt.title} in resolution {video_stream.resolution}")
        video_file_path = os.path.join(output_path, yt.title + "_video.mp4")
        video_file_size = video_stream.filesize

        with tqdm(total=video_file_size, unit='B', unit_scale=True, desc="Video Download", ascii=True) as progress_bar:
            def on_video_progress(stream, chunk, bytes_remaining):
                progress_bar.update(len(chunk))

            yt.register_on_progress_callback(on_video_progress)
            video_stream.download(output_path=output_path, filename=yt.title + "_video.mp4")

        # Download audio with progress bar
        print(f"\nDownloading audio: {yt.title} with bitrate {audio_stream.abr}")
        audio_file_path = os.path.join(output_path, yt.title + "_audio.mp4")
        audio_file_size = audio_stream.filesize

        with tqdm(total=audio_file_size, unit='B', unit_scale=True, desc="Audio Download", ascii=True) as progress_bar:
            def on_audio_progress(stream, chunk, bytes_remaining):
                progress_bar.update(len(chunk))

            yt.register_on_progress_callback(on_audio_progress)
            audio_stream.download(output_path=output_path, filename=yt.title + "_audio.mp4")

        # Merge video and audio using ffmpeg
        merged_file_path = os.path.join(output_path, yt.title + ".mp4")
        print(f"\nMerging video and audio into: {merged_file_path}")
        subprocess.run([
            'ffmpeg', '-i', video_file_path, '-i', audio_file_path, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', merged_file_path
        ])

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
    # Get the link and directory path from the user
    url = input("Enter the YouTube video link: ")
    output_path = input("Enter the directory path to save the video (e.g., C:/Videos): ")

    # Normalize the path
    output_path = os.path.normpath(output_path.strip())

    download_youtube_video(url, output_path)

if __name__ == "__main__":
    main()