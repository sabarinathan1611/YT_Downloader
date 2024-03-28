from pytube import YouTube
import os
import random
from moviepy.editor import VideoFileClip, AudioFileClip

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
        root_path = os.path.dirname(os.path.realpath(__file__))  # Get the directory of the current script
        download_path = os.path.join(root_path, 'static/video')
        
        # Filter streams by resolution and file extension
        stream = yt.streams.filter(res=resolution, file_extension='mp4').first()
        if stream:
            # Check if the stream contains both video and audio
            if stream.includes_audio_track:
                print(f"\nDownloading '{yt.title}' in {resolution}...")
                filename = f"{yt.title}_{random_number}.mp4"
                stream.download(output_path=download_path, filename=filename)
                print("Download completed!")
                return {'success': True, 'message': 'Download completed!', 'file': filename}
            else:
                print("Selected stream does not contain audio. Attempting to download with audio merged from lowest resolution...")
                return download_video_with_merged_audio(url, resolution)
        else:
            return {'success': False, 'error': f"No stream found with specified resolution: {resolution}."}
    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        return {'success': False, 'error': error_message}

def download_video_with_merged_audio(url, resolution):
    try:
        random_number = random.randint(1000, 9999)

        yt = YouTube(url)
        print(f"Title: {yt.title}")
        
        # Filter streams by progressive streams with video and audio
        available_streams = yt.streams.filter(progressive=True, file_extension='mp4')
        
        # Sort streams by resolution from lowest to highest
        available_streams = sorted(available_streams, key=lambda x: int(x.resolution[:-1]))

        # Set download path
        root_path = os.path.dirname(os.path.realpath(__file__))  # Get the directory of the current script
        download_path = os.path.join(root_path, 'static/video')
        
        # Select the lowest resolution stream with audio
        stream_low_res_with_audio = None
        for stream in available_streams:
            if stream.includes_audio_track:
                stream_low_res_with_audio = stream
                break

        # Select the highest resolution stream without audio
        stream_high_res_without_audio = None
        for stream in available_streams[::-1]:
            if stream.resolution == resolution and not stream.includes_audio_track:
                stream_high_res_without_audio = stream
                break
        
        if stream_low_res_with_audio and stream_high_res_without_audio:
            # Download video without audio
            video_filename = f"{yt.title}_{random_number}_video.mp4"
            video_file_path = os.path.join(download_path, video_filename)
            stream_high_res_without_audio.download(output_path=download_path, filename=video_filename)

            # Download audio separately from low-resolution stream
            audio_filename = f"{yt.title}_{random_number}_audio.mp4"
            audio_file_path = os.path.join(download_path, audio_filename)
            stream_low_res_with_audio.download(output_path=download_path, filename=audio_filename)

            # Combine video and audio
            video_clip = VideoFileClip(video_file_path)
            audio_clip = AudioFileClip(audio_file_path)
            final_clip = video_clip.set_audio(audio_clip)
            final_filename = f"{yt.title}_{random_number}_with_audio.mp4"
            final_file_path = os.path.join(download_path, final_filename)
            final_clip.write_videofile(final_file_path)

            print("Download completed!")
            return {'success': True, 'message': 'Download completed!', 'file': final_file_path}
        else:
            print("Failed to find suitable streams for merging audio.")
            return {'success': False, 'error': "Failed to find suitable streams for merging audio."}
    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        return {'success': False, 'error': error_message}



# Example usage:
video_url = 'https://www.youtube.com/watch?v=5kUK7yK1zXI'
download_video(video_url, '720p')
