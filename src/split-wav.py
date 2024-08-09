import os
import argparse
from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_leading_silence
from glob import glob


def trim_silence(audio_chunk, silence_thresh=-50):
    """Trim silence from the start and end of the audio chunk."""
    start_trim = detect_leading_silence(audio_chunk, silence_thresh)
    end_trim = detect_leading_silence(audio_chunk.reverse(), silence_thresh)
    duration = len(audio_chunk)
    trimmed_chunk = audio_chunk[start_trim:duration-end_trim]
    return trimmed_chunk


def split_wav_file(input_file, output_folder, prefix, min_silence_len=1000, silence_thresh=-50):
    # Load the audio file
    audio = AudioSegment.from_wav(input_file)

    # Split the audio file on silence
    chunks = split_on_silence(
        audio,
        min_silence_len=min_silence_len,  # Minimum length of silence (in ms)
        silence_thresh=silence_thresh  # Consider it silent if below this threshold (in dBFS)
    )

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the base name of the input file (without extension)
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    # Export each chunk as a separate file
    for i, chunk in enumerate(chunks):
        trimmed_chunk = trim_silence(chunk, silence_thresh)

        output_file = os.path.join(output_folder, f'{prefix}{base_name}_sample_{i}.wav')
        trimmed_chunk.export(output_file, format="wav")
        print(f"Exported: {output_file}")

def process_files(input_path, output_folder, prefix, min_silence_len, silence_thresh):
    if os.path.isfile(input_path):
        # Process single file
        split_wav_file(input_path, output_folder, prefix, min_silence_len, silence_thresh)
    elif os.path.isdir(input_path):
        # Process all WAV files in the directory
        for wav_file in glob(os.path.join(input_path, '*.wav')):
            print(f"Processing: {wav_file}")
            split_wav_file(wav_file, output_folder, prefix, min_silence_len, silence_thresh)
    else:
        print(f"Error: {input_path} is not a valid file or directory")

def main():
    parser = argparse.ArgumentParser(description="Split WAV file(s) into separate samples based on silence.")
    parser.add_argument("input_path", help="Path to the input WAV file or directory containing WAV files")
    parser.add_argument("output_folder", help="Path to the output folder for individual samples")
    parser.add_argument("--prefix", default="", help="Prefix for output sample files")
    parser.add_argument("--min_silence_len", type=int, default=1000, help="Minimum length of silence (in ms)")
    parser.add_argument("--silence_thresh", type=int, default=-50, help="Silence threshold (in dBFS)")

    args = parser.parse_args()

    process_files(args.input_path, args.output_folder, args.prefix, args.min_silence_len, args.silence_thresh)

if __name__ == "__main__":
    main()