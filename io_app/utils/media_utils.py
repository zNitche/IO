import subprocess


def get_video_frames_count(file_path):
    frames_count = None
    command = f"ffprobe -v error -select_streams v:0 -count_packets " \
              f"-show_entries stream=nb_read_packets -of csv=p=0 {file_path}"
    output = subprocess.check_output(command.split())

    try:
        frames_count = int(output)
    except:
        pass

    return frames_count
