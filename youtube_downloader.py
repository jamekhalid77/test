#!/usr/bin/env python3
import os
import json
import yt_dlp
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class YouTubeDownloader:
    def __init__(self):
        self.download_folder = "downloaded_videos"
        self.channel_url = os.getenv('CHANNEL_URL', 'https://www.youtube.com/@YourChannelHere')
        self.max_downloads = int(os.getenv('MAX_DOWNLOADS', '5'))  # Limit downloads per run
        
        # Create download folder
        os.makedirs(self.download_folder, exist_ok=True)
        
    def download_videos(self):
        """Download videos from YouTube channel"""
        
        # yt-dlp options for downloading
        ydl_opts = {
            'outtmpl': f'{self.download_folder}/%(title)s_%(id)s.%(ext)s',
            'format': 'best[ext=mp4]/best',  # Download best quality MP4
            'ignoreerrors': True,
            'quiet': False,
            'no_warnings': False,
            'playlistend': self.max_downloads,  # Limit number of downloads
            'writeinfojson': True,  # Save video metadata
            'writethumbnail': True,  # Download thumbnail
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                logging.info(f"📥 Starting download from: {self.channel_url}")
                logging.info(f"📊 Max downloads per run: {self.max_downloads}")
                
                # Download videos
                ydl.download([self.channel_url])
                
                # Count downloaded files
                video_files = [f for f in os.listdir(self.download_folder) if f.endswith('.mp4')]
                
                logging.info(f"✅ Download completed!")
                logging.info(f"📁 Total videos downloaded: {len(video_files)}")
                
                # List downloaded videos
                logging.info("📹 Downloaded videos:")
                for video in video_files[:10]:  # Show first 10
                    logging.info(f"   - {video}")
                
                return True
                
        except Exception as e:
            logging.error(f"❌ Download error: {e}")
            return False
    
    def get_stats(self):
        """Get download statistics"""
        try:
            video_files = [f for f in os.listdir(self.download_folder) if f.endswith('.mp4')]
            json_files = [f for f in os.listdir(self.download_folder) if f.endswith('.json')]
            thumb_files = [f for f in os.listdir(self.download_folder) if f.endswith(('.jpg', '.webp', '.png'))]
            
            total_size = sum(os.path.getsize(os.path.join(self.download_folder, f)) 
                           for f in os.listdir(self.download_folder)) / (1024*1024)  # MB
            
            stats = {
                'timestamp': datetime.now().isoformat(),
                'total_videos': len(video_files),
                'total_metadata_files': len(json_files),
                'total_thumbnails': len(thumb_files),
                'total_size_mb': round(total_size, 2),
                'download_folder': self.download_folder
            }
            
            # Save stats to file
            with open('download_stats.json', 'w') as f:
                json.dump(stats, f, indent=2)
            
            logging.info("📊 Statistics saved to download_stats.json")
            return stats
            
        except Exception as e:
            logging.error(f"Error getting stats: {e}")
            return {}

def main():
    print("="*60)
    print("🎬 YOUTUBE VIDEO DOWNLOADER")
    print("="*60)
    
    downloader = YouTubeDownloader()
    
    # Download videos
    success = downloader.download_videos()
    
    if success:
        # Get and display statistics
        stats = downloader.get_stats()
        
        print("\n" + "="*60)
        print("📊 DOWNLOAD STATISTICS")
        print("="*60)
        print(f"Total Videos: {stats.get('total_videos', 0)}")
        print(f"Total Size: {stats.get('total_size_mb', 0)} MB")
        print(f"Metadata Files: {stats.get('total_metadata_files', 0)}")
        print(f"Thumbnails: {stats.get('total_thumbnails', 0)}")
        print("="*60)
        
        logging.info("✅ Process completed successfully!")
    else:
        logging.error("❌ Download process failed!")
        exit(1)

if __name__ == "__main__":
    main()
