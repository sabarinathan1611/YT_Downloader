from flask import Flask, request, jsonify
from pytube import YouTube
import os
from flask_cors import CORS
import random
from flask import send_from_directory

from moviepy.editor import VideoFileClip, AudioFileClip
app = Flask(__name__)
CORS(app)
FOLDER = os.path.join(app.root_path, 'static/video')
app.config['FOLDER'] = FOLDER


def download_video(url, resolution):
    try:
        random_number = random.randint(1000, 9999)

        yt = YouTube(url)
        print(f"Title: {yt.title}")
        
        # Print available streams
        available_streams = yt.streams.filter(progressive=True, file_extension='mp4')
        print("Available Streams:")
        for stream in available_streams:
            print(f"- Resolution: {stream.resolution}, FPS: {stream.fps}, Video Codec: {stream.video_codec}, Audio Codec: {stream.audio_codec}")
        
        # Set download path
        download_path = app.config['FOLDER']
        
        # Filter streams by resolution and file extension
        stream = yt.streams.filter(res=resolution, file_extension='mp4').first()
        if stream:
            # Check if the stream contains both video and audio
            if stream.includes_audio_track:
                print(f"\nDownloading '{yt.title}' in {resolution}...")
                filename = f"Video_{random_number}.mp4"
                stream.download(output_path=download_path, filename=filename)
                print("Download completed!")
                return {'success': True, 'message': 'Download completed!', 'file': filename}
            else:
                print("Selected stream does not contain audio.")
                return {'success': False, 'error': 'Selected stream does not contain audio.'}
        else:
           
          return {'success': False, 'error': 'Selected stream does not contain audio.'}
    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        return {'success': False, 'error': error_message}
    
# def download_video_with_audio(url, resolution):
#     try:
#         random_number = random.randint(1000, 9999)

#         yt = YouTube(url)
#         print(f"Title: {yt.title}")
        
#         # Print available streams
#         available_streams = yt.streams.filter(progressive=True, file_extension='mp4')
        
#         for stream in available_streams:
#             print(f"- Resolution: {stream.resolution}, FPS: {stream.fps}, Video Codec: {stream.video_codec}, Audio Codec: {stream.audio_codec}")
        
#         # Set download path
#         download_path = app.config['FOLDER']
        
#         # Filter streams by resolution and file extension
#         stream_without_audio = yt.streams.filter(res=resolution, file_extension='mp4', only_video=True).first()
#         stream_with_audio = yt.streams.filter(res='144p', file_extension='mp4', only_audio=True).first()
        
#         if stream_without_audio and stream_with_audio:
#             # Download video without audio
#             video_filename = f"{yt.title}_{random_number}_video.mp4"
#             video_file_path = os.path.join(download_path, video_filename)
#             stream_without_audio.download(output_path=download_path, filename=video_filename)

#             # Download audio separately
#             audio_filename = f"{yt.title}_{random_number}_audio.mp4"
#             audio_file_path = os.path.join(download_path, audio_filename)
#             stream_with_audio.download(output_path=download_path, filename=audio_filename)

#             # Combine video and audio
#             video_clip = VideoFileClip(video_file_path)
#             audio_clip = AudioFileClip(audio_file_path)
#             final_clip = video_clip.set_audio(audio_clip)
#             final_filename = f"{yt.title}_{random_number}_with_audio.mp4"
#             final_file_path = os.path.join(download_path, final_filename)
#             final_clip.write_videofile(final_file_path)

#             print("Download completed!")
#             return {'success': True, 'message': 'Download completed!', 'file': final_file_path}
#         else:
#             print(f"No stream found with specified resolution: {resolution}.")
#             return {'success': False, 'error': f"No stream found with specified resolution: {resolution}."}
#     except Exception as e:
#         error_message = f"An error occurred: {e}"
#         print(error_message)
#         return {'success': False, 'error': error_message}

    
@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    try:
        folder = app.config['FOLDER']
        
        response = send_from_directory(folder, filename, as_attachment=True)
        
        
        
        
        return response
    except Exception as e:
        return str(e), 404
    # finally:
    #     path = os.path.join(folder, filename)
    #     os.remove(path)


@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    video_url = data.get('video_url')
    resolution = data.get('resolution')
    
    if video_url:
        result = download_video(video_url,resolution)
        return jsonify(result)
    else:
        return jsonify({'success': False, 'error': 'No video URL provided.'})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
