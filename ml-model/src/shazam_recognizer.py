import asyncio
from shazamio import Shazam
import os
from typing import Dict, Optional, Union

class ShazamRecognizer:
    def __init__(self):
        self.shazam = Shazam()
    
    async def recognize_audio_file(self, file_path: str) -> Dict:
        """
        Recognize a song from an audio file using Shazam.
        
        Args:
            file_path: Path to the audio file to recognize
            
        Returns:
            Dict: {
                'success': bool,
                'track': {
                    'title': str,
                    'artist': str,
                    'year': Optional[int],
                    'album': Optional[str],
                    'genre': Optional[str],
                    'lyrics': Optional[str],
                    'artwork_url': Optional[str],
                    'shazam_url': Optional[str]
                },
                'error': Optional[str]
            }
        """
        if not os.path.exists(file_path):
            return {
                'success': False,
                'error': f'File not found: {file_path}'
            }
        
        try:
            # Recognize the song
            result = await self.shazam.recognize_song(file_path)
            
            if not result or 'track' not in result:
                return {
                    'success': False,
                    'error': 'No match found or unable to recognize the song'
                }
            
            # Extract relevant information
            track = result.get('track', {})
            sections = track.get('sections', [])
            metadata = track.get('hub', {})
            
            # Get lyrics if available
            lyrics = None
            for section in sections:
                if section.get('type') == 'LYRICS':
                    lyrics = section.get('text', [])
                    if isinstance(lyrics, list):
                        lyrics = '\n'.join(lyrics)
                    break
            
            # Get artwork
            artwork_url = None
            if 'images' in track and 'coverart' in track['images']:
                artwork_url = track['images']['coverart']
            
            # Get genre
            genre = None
            if 'genres' in track and 'primary' in track['genres']:
                genre = track['genres']['primary']
            
            # Get release year
            year = None
            if 'release' in metadata and 'release' in metadata['release']:
                year = metadata['release']['release']
            elif 'year' in track:
                year = track['year']
            
            # Get Shazam URL
            shazam_url = None
            if 'url' in track:
                shazam_url = track['url']
            
            return {
                'success': True,
                'track': {
                    'title': track.get('title', 'Unknown Title'),
                    'artist': track.get('subtitle', 'Unknown Artist'),
                    'year': int(year) if year and str(year).isdigit() else None,
                    'album': track.get('sections', [{}])[0].get('metadata', [{}])[0].get('text')
                            if track.get('sections') else None,
                    'genre': genre,
                    'lyrics': lyrics,
                    'artwork_url': artwork_url,
                    'shazam_url': shazam_url
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error recognizing song: {str(e)}'
            }

# Example usage
async def main():
    recognizer = ShazamRecognizer()
    
    # Example file path - replace with your audio file
    audio_file = 'path/to/your/audio_file.mp3'
    
    result = await recognizer.recognize_audio_file(audio_file)
    
    if result['success']:
        track = result['track']
        print("\n=== Song Recognized! ===")
        print(f"Title: {track['title']}")
        print(f"Artist: {track['artist']}")
        if track['year']:
            print(f"Year: {track['year']}")
        if track['album']:
            print(f"Album: {track['album']}")
        if track['genre']:
            print(f"Genre: {track['genre']}")
        if track['artwork_url']:
            print(f"Artwork: {track['artwork_url']}")
        if track['shazam_url']:
            print(f"View on Shazam: {track['shazam_url']}")
    else:
        print(f"\nRecognition failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    asyncio.run(main())
