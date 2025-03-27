def strip_directory_and_extension(file_path):
    # Get the file name without directory
    file_name = os.path.basename(file_path)
    # Remove the file extension
    file_name_without_extension = os.path.splitext(file_name)[0]
    return file_name_without_extension


# Function to get metadata for MP3 files using eyed3
def get_mp3_metadata(file_path):
    try:
        audio_file = eyed3.load(file_path)
        artist = audio_file.tag.artist or "Unknown Artist"
        album = audio_file.tag.album or "Unknown Album"
        title = audio_file.tag.title or strip_directory_and_extension(file_path)
        return artist, album, title
    except Exception as e:
        print(f"Error reading metadata from {file_path}: {e}")
        return None, None, None

# Function to get metadata for other audio files using tinytag
def get_other_metadata(file_path):
    try:
        tag = TinyTag.get(file_path)
        artist = tag.artist or "Unknown Artist"
        album = tag.album or "Unknown Album"
        title = tag.title or strip_directory_and_extension(file_path)
        return artist, album, title
    except Exception as e:
        print(f"Error reading metadata from {file_path}: {e}")
        return None, None, None

# Function to create the symlink
def create_symlink(source_file, target_path):
    try:
        # Create any intermediate directories
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        # Remove the symlink if it already exists
        if os.path.islink(target_path):
            os.remove(target_path)
        # Create the symlink
        os.symlink(source_file, target_path)
        print(f"Created symlink: {target_path}")
    except Exception as e:
        print(f"Error creating symlink for {source_file}: {e}")
