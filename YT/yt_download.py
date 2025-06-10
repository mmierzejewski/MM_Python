from pytubefix import YouTube
import os
from tqdm import tqdm
from moviepy.editor import VideoFileClip, AudioFileClip
import tempfile


def download_youtube_video(url, output_path):
    try:
        # Sprawdzanie, czy katalog istnieje, jeśli nie - próba jego utworzenia
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Tworzenie obiektu YouTube z podanego linku
        yt = YouTube(url)

        # Pobieranie dostępnych strumieni wideo w formacie mp4
        video_streams = yt.streams.filter(only_video=True, file_extension='mp4').order_by('resolution').desc()
        if not video_streams:
            video_streams = yt.streams.filter(file_extension='mp4').order_by('resolution').desc()

        # Pobieranie dostępnych strumieni audio
        audio_streams = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc()

        if not video_streams or not audio_streams:
            print("Nie znaleziono odpowiednich strumieni wideo lub audio w formacie mp4.")
            return

        # Wyświetlanie dostępnych rozdzielczości wideo
        print("\nDostępne rozdzielczości wideo:")
        for i, stream in enumerate(video_streams, 1):
            print(f"{i}. {stream.resolution} ({stream.fps}fps, {stream.mime_type})")

        # Pobieranie wyboru rozdzielczości wideo
        while True:
            try:
                video_choice = int(input("Wybierz numer rozdzielczości wideo (1-{}): ".format(len(video_streams))))
                if 1 <= video_choice <= len(video_streams):
                    break
                print("Nieprawidłowy numer. Wybierz numer od 1 do {}.".format(len(video_streams)))
            except ValueError:
                print("Podaj prawidłowy numer.")

        selected_video = video_streams[video_choice - 1]

        # Wyświetlanie dostępnych jakości audio
        print("\nDostępne jakości audio:")
        for i, stream in enumerate(audio_streams, 1):
            print(f"{i}. {stream.abr} ({stream.mime_type})")

        # Pobieranie wyboru jakości audio
        while True:
            try:
                audio_choice = int(input("Wybierz numer jakości audio (1-{}): ".format(len(audio_streams))))
                if 1 <= audio_choice <= len(audio_streams):
                    break
                print("Nieprawidłowy numer. Wybierz numer od 1 do {}.".format(len(audio_streams)))
            except ValueError:
                print("Podaj prawidłowy numer.")

        selected_audio = audio_streams[audio_choice - 1]

        # Tworzenie tymczasowych plików
        with tempfile.TemporaryDirectory() as temp_dir:
            video_path = os.path.join(temp_dir, "video.mp4")
            audio_path = os.path.join(temp_dir, "audio.mp4")
            output_file = os.path.join(output_path, f"{yt.title}.mp4")

            # Pobieranie wideo z paskiem postępu
            print(f"\nPobieranie wideo: {yt.title} w rozdzielczości {selected_video.resolution}")
            video_size = selected_video.filesize
            with tqdm(total=video_size, unit='B', unit_scale=True, desc="Wideo", ascii=True) as progress_bar:
                def on_progress(stream, chunk, bytes_remaining):
                    progress_bar.update(len(chunk))

                yt.register_on_progress_callback(on_progress)
                selected_video.download(output_path=temp_dir, filename="video.mp4")

            # Pobieranie audio z paskiem postępu
            print(f"Pobieranie audio: {yt.title} w jakości {selected_audio.abr}")
            audio_size = selected_audio.filesize
            with tqdm(total=audio_size, unit='B', unit_scale=True, desc="Audio", ascii=True) as progress_bar:
                def on_progress(stream, chunk, bytes_remaining):
                    progress_bar.update(len(chunk))

                yt.register_on_progress_callback(on_progress)
                selected_audio.download(output_path=temp_dir, filename="audio.mp4")

            # Łączenie wideo i audio
            print("Łączenie strumieni wideo i audio...")
            video_clip = VideoFileClip(video_path)
            audio_clip = AudioFileClip(audio_path)
            final_clip = video_clip.set_audio(audio_clip)
            final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")
            video_clip.close()
            audio_clip.close()
            final_clip.close()

        print(f"Pobrano i połączono pomyślnie jako: {output_file}")

    except Exception as e:
        print(f"Wystąpił błąd: {str(e)}")
        if "HTTP Error 400" in str(e):
            print("Możliwe przyczyny błędu HTTP 400:")
            print("- Niepoprawny lub niedostępny link do filmu.")
            print("- Film jest ograniczony (np. prywatny, regionalnie zablokowany).")
            print("- Wersja biblioteki pytubefix jest nieaktualna. Zaktualizuj: pip install --upgrade pytubefix")
            print("- YouTube zmienił strukturę strony, spróbuj użyć najnowszej wersji pytubefix.")
        print("Sprawdź link i spróbuj ponownie.")


def main():
    # Pobieranie linku i ścieżki katalogu od użytkownika
    url = input("Podaj link do filmu na YouTube: ")
    output_path = input("Podaj ścieżkę katalogu, gdzie zapisać film (np. C:/Wideo): ")

    # Normalizacja ścieżki
    output_path = os.path.normpath(output_path.strip())

    download_youtube_video(url, output_path)


if __name__ == "__main__":
    main()