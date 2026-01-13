import os

class FileManager:
    def __init__(self, base_directory="."):
        self.base_directory = base_directory

    def save_file(self, relative_path: str, content: str, encoding: str = "utf-8"):
        full_path = os.path.join(self.base_directory, relative_path)
        dir_path = os.path.dirname(full_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(full_path, "w", encoding=encoding) as f:
            f.write(content)

        print(f"Saved file to: {full_path}")
