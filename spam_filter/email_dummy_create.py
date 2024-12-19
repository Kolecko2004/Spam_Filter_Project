import os
import random
import string

def generate_random_text(length=100):
    """Generate random text of the specified length."""
    words = ["email", "test", "random", "message", "body", "subject", "meeting", "important", "hello", "spam"]
    return " ".join(random.choices(words, k=length // 5))

def generate_random_filename():
    """Generate a random filename."""
    prefix = random.choice(["email", "!meta", "note", "file"])
    suffix = random.choice([".txt", ".log"])
    name = "".join(random.choices(string.ascii_letters, k=8))
    return f"{prefix}_{name}{suffix}"

def create_dummy_files(directory, file_count):
    """Create a specified number of random dummy files in a directory."""
    os.makedirs(directory, exist_ok=True)  # Ensure the directory exists

    for _ in range(file_count):
        # Generate a random filename
        filename = generate_random_filename()

        # Ensure full path
        filepath = os.path.join(directory, filename)

        # Generate random content
        content = f"Subject: {generate_random_text(20)}\nBody:\n{generate_random_text(200)}"

        # Write the file
        with open(filepath, "w") as file:
            file.write(content)

    print(f"{file_count} dummy files created in {directory}")


# Call the function
create_dummy_files('./Home-Works/spam_filter/test_files', 10) 