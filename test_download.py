#!/usr/bin/env python3
import yt_dlp
import requests
import sys 
 
def check_ip():
    """Check current IP address"""
    try:
        response = requests.get('https://httpbin.org/ip', timeout=10)
        ip_info = response.json()
        print(f"Current IP: {ip_info['origin']}")
        return True
    except Exception as e:
        print(f"IP check failed: {e}")
        return False

def test_youtube_download():
    """Test YouTube video download"""
    # Simple test video (very short)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    ydl_opts = {
        'outtmpl': 'test_video.%(ext)s',
        'format': 'worst',  # Download lowest quality for speed
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,  # Just extract info, don't download
    }
    
    try:
        print("Testing YouTube access...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(test_url, download=False)
            print(f"✅ SUCCESS! Video title: {info.get('title', 'Unknown')}")
            print(f"Video ID: {info.get('id', 'Unknown')}")
            print("✅ YouTube IP NOT BLOCKED!")
            return True
            
    except Exception as e:
        error_msg = str(e).lower()
        if 'blocked' in error_msg or 'forbidden' in error_msg or '403' in error_msg:
            print("❌ YouTube IP BLOCKED!")
        else:
            print(f"❌ Download failed: {e}")
        return False

def main():
    print("=== Travis CI YouTube Test ===")
    
    # Check IP
    print("\n1. Checking IP address...")
    check_ip()
    
    # Test YouTube
    print("\n2. Testing YouTube access...")
    success = test_youtube_download()
    
    if success:
        print("\n🎉 TEST PASSED - Travis CI IP works with YouTube!")
        sys.exit(0)
    else:
        print("\n💀 TEST FAILED - Travis CI IP blocked by YouTube!")
        sys.exit(1)

if __name__ == "__main__":
    main()
