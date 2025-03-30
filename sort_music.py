import os
import shutil
from mutagen import File
import eyed3
import sys

DRY_RUN = 0

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


def create_directory_structure(base_dir, discnumber, tracknumber, artist, album, title, extension):
    # First letter of the artist's name
    artist_first_letter = artist[0].upper() if artist else 'Unknown'
    
    # Creating the new directory structure: <first letter of artist>\<artist name>\<album>\<track> <title>.<extension>
    if (discnumber == -1):
        artist_dir = os.path.join(base_dir, clean_filename(artist_first_letter), clean_filename(artist), clean_filename(album))
    else:
        artist_dir = os.path.join(base_dir, clean_filename(artist_first_letter), clean_filename(artist), clean_filename(album), clean_filename("Disc " + str(discnumber)))
    
    if (DRY_RUN):
        print ("I would create " + artist_dir)
    else:
        os.makedirs(artist_dir, exist_ok=True)

    # Define the full file path with the new structure
    if (tracknumber == -1):
        new_file_path = os.path.join(artist_dir, clean_filename(f"{title}{extension}"))
    else:
        new_file_path = os.path.join(artist_dir, clean_filename(f"{tracknumber:02d} {title}{extension}"))
        
    return new_file_path


def process_mp3_file(file_path, base_dir):
    audio_file = eyed3.load(file_path)
    artist = audio_file.tag.artist if audio_file.tag.artist else 'Unknown Artist'
    album = audio_file.tag.album if audio_file.tag.album else 'Unknown Album'
    
    if (audio_file.tag.title):
        title = audio_file.tag.title
    else:
        title = os.path.splitext(os.path.basename(file_path))[0]
        print("Cannot extract title information for " + file_path + ". I'm just to use " + title + " for the title")
    
    try:
        tracknumber = int(audio_file.tag.track_num) if audio_file.tag.track_num else -1
    except:
        tracknumber = -1
        
    try:
        discnumber = int(audio_file.tag.disc_num) if audio_file.tag.disc_num else -1
    except:
        discnumber = -1
    extension = '.mp3'

    new_file_path = create_directory_structure(base_dir, discnumber, tracknumber, artist, album, title, extension)
    
    # Move the file to the new directory structure
    if (DRY_RUN):
        print("I would move " + file_path + " to " + new_file_path)
    else:
        shutil.move(file_path, new_file_path)
    


def process_other_audio_file(file_path, base_dir):
    audio_file = File(file_path)
    artist = audio_file.tags.get("artist", ["Unknown Artist"])[0]
    title = audio_file.tags.get("title", ["Unknown Title"])[0]
    album = audio_file.tags.get("album", ["Unknown Album"])[0]
    if (title == "Unknown Title"):
        title = os.path.splitext(os.path.basename(file_path))[0]
        print("Cannot extract title information for " + file_path + ". I'm just to use " + title + " for the title")
    try:
        tracknumber = int(audio_file.tags.get("tracknumber", [-1])[0])
    except:
        tracknumber = -1
    try:
        discnumber = int(audio_file.tags.get("discnumber", [-1])[0])
    except:
        discnumber = -1
    extension = os.path.splitext(file_path)[1].lower()

    new_file_path = create_directory_structure(base_dir, discnumber, tracknumber, artist, album, title, extension)
    
    # Move the file to the new directory structure
    if (DRY_RUN):
        print("I would move " + file_path + " to " + new_file_path)
    else:
        shutil.move(file_path, new_file_path)


def organize_music_files(input_dir, output_dir):
    # Loop through the files in the input directory
    for root, _, files in os.walk(input_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith('.mp3'):
                process_mp3_file(file_path, output_dir)
            elif file.lower().endswith(('.flac', '.wav', '.ogg', '.m4a')):
                process_other_audio_file(file_path, output_dir)
            else:
                print(f"Skipping unsupported file format: {file}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    if (DRY_RUN):
        print("DRY RUN MODE ENABLED - I'LL MOVE NOTHING")
    # Specify the input directory (where your music files are)
    input_directory = "e:\\lucy\\music\\incoming"
    # Specify the output directory (where to organize the files)
    output_directory = "e:\\lucy\\music"
    
    organize_music_files(input_directory, output_directory)
    print("Music files have been organized.")