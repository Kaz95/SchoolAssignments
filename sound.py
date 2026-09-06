import io
import wave
import winsound

CHANNELS = 2
SAMPLE_WIDTH = 2
SAMPLE_RATE = 44100

input_wav_path = r'C:\Users\kazac\Downloads\kaching.wav'
raw_output_path = r'raw_audio_bytes.raw'

def extract_audio_bytes(wav_file):
    with wave.open(wav_file, 'rb') as wav_file:
        channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        sample_rate = wav_file.getframerate()
        num_frames = wav_file.getnframes()

    raw_audio_bytes = wav_file.readframes(num_frames)

    print(f'{len(raw_audio_bytes)} raw bytes.')
    print(f'Channels: {channels}      Width: {sample_width} bytes')
    print(f'sample: {sample_rate}     nframes: {num_frames}')

    return raw_audio_bytes

def write_raw_audio_bytes(file_name, raw_audio_bytes):
    with open(file_name, "wb") as raw_file:
        raw_file.write(raw_audio_bytes)



def load_raw_audio_bytes(file_path):
    with open(file_path, "rb") as raw_file:
        loaded_bytes = raw_file.read()
        return loaded_bytes



def play(loaded_bytes):
    # How have I never used io library before now?!
    bytes_io = io.BytesIO()
    # Set header and load
    with wave.open(bytes_io, "wb") as wav_write:
        wav_write.setnchannels(CHANNELS)
        wav_write.setsampwidth(SAMPLE_WIDTH)
        wav_write.setframerate(SAMPLE_RATE)
        wav_write.writeframes(loaded_bytes)

    print('playback started')
    winsound.PlaySound(bytes_io.getvalue(), winsound.SND_MEMORY)
    print('playback finished.')

if __name__ == '__main__':
    play(load_raw_audio_bytes(raw_output_path))