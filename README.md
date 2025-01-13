# WAV Splitter

WAV Splitter is a Python application with a graphical user interface that allows users to split WAV audio files into multiple samples based on periods of silence. This tool is useful for breaking down long audio recordings into individual segments or for preprocessing audio data for further analysis.

## Features

- User-friendly graphical interface
- Support for processing multiple WAV files or entire folders
- Customizable silence detection parameters
- Cross-platform compatibility (Windows, macOS, Linux)
- Multithreaded processing for responsive UI during long operations

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- pip (Python package installer)
- Xcode Command Line Tools (for macOS users)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/alexanderwanyoike/wav-splitter.git
   cd wav-splitter
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Unix or MacOS:
     ```
     source venv/bin/activate
     ```
   - On Windows:
     ```
     venv\Scripts\activate
     ```

4. Install wxPython:
   - On macOS:
     ```
     pip install -U wxPython
     ```
   - If the above command fails on macOS, you may need to install wxPython using Homebrew:
     ```
     brew update
     brew install wxpython
     pip install -U wxPython
     ```
   - On Linux:
     ```
     pip install -U -f https://wxpython.org/Phoenix/snapshot-builds/ wxPython
     ```
   - On Windows:
     ```
     pip install -U wxPython
     ```

5. Install the remaining required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the WAV Splitter application:

1. Ensure you're in the project directory and your virtual environment is activated.

2. Run the main script:
   ```
   python split_wav_gui.py
   ```

3. Use the graphical interface to:
   - Add input WAV files or folders
   - Select an output folder
   - Set processing parameters (prefix, minimum silence length, silence threshold)
   - Click "Split WAV" to process the files

## Building Standalone Executable (macOS)

1. Ensure you're in the project directory and your virtual environment is activated.

2. Install py2app:
   ```
   pip install py2app
   ```

3. Build the application:
   ```
   python setup.py py2app
   ```

4. Find the standalone application in the `dist` folder.

## Troubleshooting

- If you encounter issues with wxPython installation, please refer to the [official wxPython installation guide](https://wxpython.org/pages/downloads/).
- On macOS, if you face problems related to the "Python.h" header file not being found, you may need to install the macOS SDK headers:
  ```
  open /Library/Developer/CommandLineTools/Packages/macOS_SDK_headers_for_macOS_10.14.pkg
  ```

## Contributing

Contributions to the WAV Splitter project are welcome. Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [pydub](https://github.com/jiaaro/pydub) for audio processing
- [wxPython](https://www.wxpython.org/) for the graphical user interface
