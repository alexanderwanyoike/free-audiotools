import unittest
import os
import tempfile
import shutil
from pydub import AudioSegment
from pydub.generators import Sine
from ..split_wav_core import trim_silence, split_wav_file, process_files

class TestSplitWavCore(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        
        # Create a test WAV file
        self.test_wav = os.path.join(self.test_dir, "test.wav")
        audio = AudioSegment.silent(duration=5000)  # 5 seconds of silence
        audio = audio.overlay(Sine(440).to_audio_segment(duration=1000), position=1000)  # Add a 1-second tone at 1 second
        audio = audio.overlay(Sine(440).to_audio_segment(duration=1000), position=3000)  # Add another 1-second tone at 3 seconds
        audio.export(self.test_wav, format="wav")

    def tearDown(self):
        # Remove the temporary directory and its contents
        shutil.rmtree(self.test_dir)

    def test_trim_silence(self):
        audio = AudioSegment.from_wav(self.test_wav)
        trimmed = trim_silence(audio)
        self.assertLess(len(trimmed), len(audio), "Trimmed audio should be shorter than original")

    def test_split_wav_file(self):
        output_folder = os.path.join(self.test_dir, "output")
        os.makedirs(output_folder)
        
        samples = list(split_wav_file(self.test_wav, output_folder, "test_", 500, -50))
        
        self.assertEqual(len(samples), 2, "Should have created 2 samples")
        for sample in samples:
            self.assertTrue(os.path.exists(sample.split(": ")[1]), "Sample file should exist")

    def test_process_files(self):
        output_folder = os.path.join(self.test_dir, "output")
        os.makedirs(output_folder)
        
        log = []
        def update_callback(message):
            log.append(message)
        
        def complete_callback():
            log.append("Complete")
        
        process_files([self.test_wav], output_folder, "test_", 500, -50, update_callback, complete_callback)
        
        self.assertIn("Processing file: " + self.test_wav, log, "Should have logged processing of test file")
        self.assertIn("Complete", log, "Should have called complete callback")
        self.assertTrue(any("Exported: " in message for message in log), "Should have exported at least one file")

if __name__ == '__main__':
    unittest.main()