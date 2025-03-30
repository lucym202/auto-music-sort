import os
import shutil
import eyed3
import sys
from mutagen import File
DRY_RUN = 1

def clean_filename(filename):
    filename = filename.replace("\\","-")
    filename = filename.replace("/","-")
    filename = filename.replace(":","-")
    filename = filename.replace("*","")
    filename = filename.replace("?","")
    filename = filename.replace('"',"")
    filename = filename.replace("<","(")
    filename = filename.replace(">",")")
    filename = filename.replace("|","")
    return filename

def get_music_files(root_dir, exclude_dir):
    """Recursively find all music files in the given directory."""
    music_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(('.mp3', '.flac', '.wav', '.m4a')):  # You can add more formats here
                if not (dirpath.lower().startswith(exclude_dir.lower())):
                    music_files.append(os.path.join(dirpath, filename))
    return music_files

def get_metadata(file_path):
    """Extract album and artist metadata from the music file."""
    if file_path.lower().endswith('.mp3'):
        try:
            audiofile = eyed3.load(file_path)
            album = audiofile.tag.album
            artist = audiofile.tag.artist
            return album, artist
        except Exception as e:
            print(f"Error reading metadata for {file_path}: {e}")
            return None, None
    else:
        try:
            audio_file = File(file_path)
            artist = audio_file.tags.get("artist", ["Unknown Artist"])[0]
            album = audio_file.tags.get("album", ["Unknown Album"])[0]
            return album, artist
        except Exception as e:
            print(f"Error reading metadata for {file_path}: {e}")
            return None, None

def find_compilations(music_files, excluded_albums):
    """Find music files that belong to compilations (same album, different artists)."""
    album_artist_map = {}
    
    # Map files by album and collect artists for each album
    print("===== Recurse directories =====")
    for file_path in music_files:
        print("Scanning " + file_path)
        album, artist = get_metadata(file_path)
        if album and artist:
            if album not in album_artist_map:
                album_artist_map[album] = set()
            album_artist_map[album].add(artist)
    
    # Filter albums that have more than one artist (compilations)
    print("===== Filter compilations =====")
    compilations = {}
    for album, artists in album_artist_map.items():
        if len(artists) > 1:  # This is a compilation, because it has multiple artists
            print("Identified compilation: " + album)
            if(album == excluded_albums):
                print("In Exclude List")
            else:
                compilations[album] = artists
    
    return compilations

def move_files_to_album_folder(compilations, music_files, target_base_dir):
    """Move compilation files to a new folder and create symlinks."""
    for album, artists in compilations.items():
        album_folder = os.path.join(target_base_dir, clean_filename(album))
        if (DRY_RUN == 0):
            os.makedirs(album_folder, exist_ok=True)
        
        for file_path in music_files:
            album_metadata, artist_metadata = get_metadata(file_path)
            if album_metadata == album and artist_metadata in artists:
                # Move file to the album folder
                filename = os.path.basename(file_path)
                target_path = os.path.join(album_folder, filename)

                # Avoid overwriting if the file already exists in the destination folder
                
                if not os.path.exists(target_path):
                    if (DRY_RUN == 0):
                        shutil.move(file_path, target_path)
                    print(f"Moved: {file_path} -> {target_path}")
                    if (DRY_RUN == 0):
                        os.symlink(target_path, file_path)
                    print(f"Created symlink: {file_path} -> {target_path}")
                else:
                    print(f"Skipped (file exists): {file_path}")
                

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if (DRY_RUN != 0):
        print("Dry run, no FS changes made")
        
    # Set the root directory where your music files are
    root_dir = 'e:\\lucy\\music'
    
    # Set the base target directory where albums should be moved
    target_base_dir = 'e:\\lucy\\music\\compilations'
    
    exclude_dir = (target_base_dir, "e:\\lucy\\music\\incoming")
    excluded_albums = ("gold","greatest hits","Le quattro stagioni","out of exile","dude ranch","keep on skanking","african herbsman","satisfy my soul","be happy ! despite it all...","the best of","the catalogue flexi disc","we are the world?","settle","2001","metallica","reload","the hunting of the snark","lady of the dawn","tribute","in search of...","pacifier","crash! boom! bang! (extended edition)","home","reel fine blend","blue light disco","no pads no hemlets... just balls","cosmic thing","the best of van morrison","we'll meet again, the very best of vera lynn",'"weird al" yankovic',"alapalooza")
    
    # Get all music files
    print("================ Scan Music Files =================")
    music_files = get_music_files(root_dir, target_base_dir)
    
    print("============== Identify Compilations ==============")
    # Find compilations (same album, different artists)
    compilations = find_compilations(music_files, excluded_albums)

    print("========== Move and symlink operations ============")    
    # Move files and create symlinks for compilations
    move_files_to_album_folder(compilations, music_files, target_base_dir)

if __name__ == "__main__":
    main()