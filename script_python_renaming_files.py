import os
import re
from bs4 import BeautifulSoup
from unidecode import unidecode

# Directory paths
source_directory = "source"
target_directory = "target"

# Ask the user for the source_directory, target_directory, and html_content
source_directory = input("Please enter the source directory (default: 'source'): ") or "source"
target_directory = input("Please enter the target directory (default: 'target'): ") or "target"
html_content = input("Please enter the HTML content (default: 'html_content'): ") or "html_content"

# Verify if the source and target directories exist
if not os.path.exists(source_directory):
    print("Source directory not found.")
    exit()
if not os.path.exists(target_directory):
    os.makedirs(target_directory)

# Print the user responses
print("Source directory: ", source_directory)
print("Target directory: ", target_directory)
print("HTML content: ", html_content)

# Ask for confirmation or update
confirm = input("Is this information correct? (yes/no): ").lower()
if confirm in ['y', 'yes']:
    pass
elif confirm in ['n', 'no']:
    print("Please run the script again and enter the correct information.")
    exit()
else:
    print("Invalid input. Please enter 'yes' or 'no'.")

# Retrieve the text from the HTML file
def retrieve_text_from_html(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
        soup = BeautifulSoup(html_content, "html.parser")
        current_lesson_div = soup.find("div", class_="current-lesson")
        if current_lesson_div:
            link_contents = current_lesson_div.find_all("a", class_="link")
            # Extract and concatenate the text from anchor tags
            concatenated_text = "".join(link.get_text() for link in link_contents)
            return concatenated_text.strip()
        else:
            return None

# Replace spaces, slashes, colons, and periods with underscores, remove accents, and replace "'" with "-"
def transform_text(text):
    # Remove accents and replace "'" with "-"
    cleaned_text = re.sub(r"[^a-zA-Z0-9\s./:'-]", "", unidecode(text))
    underscored_text = re.sub(r"[\s./:'-]+", "_", cleaned_text)
    # Add an underscore before each digit that follows a letter
    underscored_text = re.sub(r"(?<=[a-zA-Z])(?=\d)", "_", underscored_text)
    words = underscored_text.split("_")
    camel_case_text = "_".join(word.capitalize() for word in words)
    return camel_case_text

# Rename the HTML file with the transformed text
def rename_html_file(file_path, new_name):
    file_name = os.path.basename(file_path)
    file_extension = os.path.splitext(file_name)[1]
    new_file_name = new_name + file_extension
    new_file_path = os.path.join(target_directory, new_file_name)
    os.rename(file_path, new_file_path)

# Print a message before the loop
print("Starting processing HTML files...")

# Iterate through the HTML files in the source directory
for file_name in os.listdir(source_directory):
    if file_name.endswith(".html"):
        file_path = os.path.join(source_directory, file_name)
        # Retrieve the text from the HTML file
        text = retrieve_text_from_html(file_path)
        if text:
            # Transform the text
            transformed_text = transform_text(text)
            # Debug: Print the original and transformed text
            print(f"Original Text: {text}")
            print(f"Transformed Text: {transformed_text}")
            # Rename the HTML file
            rename_html_file(file_path, transformed_text)

# Print a message after the loop
print("Finished processing HTML files.")
