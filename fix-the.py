import os
import shutil

# Define the path of the 'T' directory
music_dir = "e:\\lucy\\music"
T_dir = os.path.join(music_dir, "T")

# Function to find subdirectories starting with 'the'
def move_subdirectories():
    # Loop through all the items in the T directory
    for item in os.listdir(T_dir):
        item_path = os.path.join(T_dir, item)

        # Check if the item is a directory and its name starts with 'the'
        if os.path.isdir(item_path) and item.lower().startswith("the"):
            # Split the name to extract the second word
            words = item.split()
            if len(words) > 1:
                second_word = words[1].upper()

                # Define the target directory, which is the first letter of the second word
                target_dir = os.path.join(music_dir, second_word[0])

                # Create the target directory if it does not exist
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)

                # Move the subdirectory to the target directory
                target_path = os.path.join(target_dir, item)
                shutil.move(item_path, target_path)
                print(f"Moved '{item}' to '{target_path}'")

# Run the function
move_subdirectories()
