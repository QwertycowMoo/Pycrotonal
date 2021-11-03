# fa21-cs242-project

# Audio settings
Make sure that your computer's audio settings are set up with a 48000Hz sample rate. This will avoid any aliasing that may happen with FM and higher pitches.

# Testing
Navigate to the `pycrotonal` file directory. Run `python -m tests.test_(package)` to run the tests. This is because of the weird way that Python imports its modules and how \_\_init\_\_.py creates a packages that can then be imported.