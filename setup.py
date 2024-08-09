from setuptools import setup


APP = ['src/split_wav_gui.py']
DATA_FILES = ['src/split_wav_core.py']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['wx', 'pydub'],
    'iconfile': 'icon/icon.icns',  # Optional: Add an icon for your app
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
