import importlib
import inspect
import os

folder_path = os.path.dirname(__file__)

for root, _, files in os.walk(folder_path):
    for file in files:
        if file.endswith(".py") and file != "__init__.py":
            relative_path = os.path.relpath(os.path.join(root, file), folder_path)
            module_path = relative_path.replace(os.sep, ".").replace(".py", "")
            module = importlib.import_module(f".{module_path}", package="strategies")

            for name, obj in inspect.getmembers(module, inspect.isclass):
                globals()[name] = obj