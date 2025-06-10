from pytubefix import YouTube
import os
from tqdm import tqdm


def download_youtube_video(url, output_path):
    try:
        # Sprawdzanie, czy katalog istnieje, jeśli nie - próba jego utworzenia
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Tworzenie obiektu YouTube z podanego linku
        yt = YouTube(url)

        # Pobieranie dostępnych strumieni wideo w formacie mp4
        video_streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()

        if not video_streams:
            video_streams = yt.streams.filter(file_extension='mp4').order_by('resolution').desc()

        if not video_streams:
            print("Nie znaleziono odpowiednich strumieni wideo w formacie mp4.")
            return

        # Wyświetlanie dostępnych rozdzielczości
        print("\nDostępne rozdzielczości:")
        for i, stream in enumerate(video_streams, 1):
            print(f"{i}. {stream.resolution} ({stream.fps}fps, {stream.mime_type})")

        # Pobieranie wyboru użytkownika
        while True:
            try:
                choice = int(input("Wybierz numer rozdzielczości (1-{}): ".format(len(video_streams))))
                if 1 <= choice <= len(video_streams):
                    break
                print("Nieprawidłowy numer. Wybierz numer od 1 do {}.".format(len(video_streams)))
            except ValueError:
                print("Podaj prawidłowy numer.")

        selected_stream = video_streams[choice - 1]

        # Pobieranie filmu z paskiem postępu
        print(f"\nPobieranie: {yt.title} w rozdzielczości {selected_stream.resolution}")

        # Pobieranie rozmiaru pliku
        file_size = selected_stream.filesize

        # Pobieranie pliku z użyciem paska postępu
        with tqdm(total=file_size, unit='B', unit_scale=True, desc="Postęp", ascii=True) as progress_bar:
            def on_progress(stream, chunk, bytes_remaining):
                progress_bar.update(len(chunk))

            yt.register_on_progress_callback(on_progress)
            selected_stream.download(output_path=output_path)

        print(f"Pobrano pomyślnie jako: {os.path.join(output_path, yt.title + '.mp4')}")

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