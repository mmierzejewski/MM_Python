from pytube import YouTube
import os

def download_youtube_video(url):
    try:
        # Tworzenie obiektu YouTube z podanego linku
        yt = YouTube(url)
        
        # Wybór strumienia wideo w formacie mp4 z najwyższą rozdzielczością
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        
        if not video_stream:
            print("Nie znaleziono odpowiedniego strumienia wideo w formacie mp4.")
            return
        
        # Pobieranie filmu do bieżącego katalogu
        print(f"Pobieranie: {yt.title}")
        video_stream.download()
        print(f"Pobrano pomyślnie jako: {yt.title}.mp4")
        
    except Exception as e:
        print(f"Wystąpił błąd: {str(e)}")

def main():
    # Pobieranie linku od użytkownika
    url = input("Podaj link do filmu na YouTube: ")
    download_youtube_video(url)

if __name__ == "__main__":
    main()