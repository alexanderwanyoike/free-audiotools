import os
from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_leading_silence
from glob import glob

def trim_silence(audio_chunk, silence_thresh=-50):
    start_trim = detect_leading_silence(audio_chunk, silence_thresh)
    end_trim = detect_leading_silence(audio_chunk.reverse(), silence_thresh)
    duration = len(audio_chunk)
    trimmed_chunk = audio_chunk[start_trim:duration-end_trim]
    return trimmed_chunk

def split_wav_file(input_file, output_folder, prefix, min_silence_len=1000, silence_thresh=-50):
    audio = AudioSegment.from_wav(input_file)
    chunks = split_on_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh
    )

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    base_name = os.path.splitext(os.path.basename(input_file))[0]

    for i, chunk in enumerate(chunks):
        trimmed_chunk = trim_silence(chunk, silence_thresh)
        output_file = os.path.join(output_folder, f'{prefix}{base_name}_sample_{i}.wav')
        trimmed_chunk.export(output_file, format="wav")
        yield f"Exported: {output_file}"

def process_files(input_paths, output_folder, prefix, min_silence_len, silence_thresh, update_callback, complete_callback):
    try :
        for input_path in input_paths:
            if os.path.isfile(input_path):
                update_callback(f"Processing file: {input_path}")
                for message in split_wav_file(input_path, output_folder, prefix, min_silence_len, silence_thresh):
                    update_callback(message)
            elif os.path.isdir(input_path):
                for wav_file in glob(os.path.join(input_path, '*.wav')):
                    update_callback(f"Processing: {wav_file}")
                    for message in split_wav_file(wav_file, output_folder, prefix, min_silence_len, silence_thresh):
                        update_callback(message)
            else:
                update_callback(f"Error: {input_path} is not a valid file or directory")
    finally:
        complete_callback()