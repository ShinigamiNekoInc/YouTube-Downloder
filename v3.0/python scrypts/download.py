import os
from yt_dlp import YoutubeDL


def download_best_video(url: str, output_dir: str = './downloads'):
  os.makedirs(output_dir, exist_ok=True)

  ydl_opts = {
      'format': 'bestvideo+bestaudio/best',
      'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
      'merge_output_format': 'mkv',
      'ffmpeg_location': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ffmpeg', 'bin')
  }

  try:
    with YoutubeDL(ydl_opts) as ydl:
      print(f'Начинаю загрузку: {url}')
      ydl.download([url])
      print('Загрузка успешно завершена!')
  except Exception as e:
    print(f'Произошла ошибка: {e}')


if __name__ == '__main__':
  video_url = input('Введите ссылку на YouTube видео: ').strip()
  if video_url:
    download_best_video(video_url)
