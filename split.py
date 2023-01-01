import os
import subprocess

# Set the input and output directories relative to the script folder
input_dir = 'input'
output_dir = 'output'

# Set the input and output file names
input_filename = 'input.mp4'
output_filename_template = 'output_{}.mp4'

# Set the duration of each part in seconds
part_duration = 12 * 60

# Create the input and output directories if they do not exist
if not os.path.exists(input_dir):
    os.makedirs(input_dir)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Calculate the total number of parts
video_info = subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                     '-of', 'default=noprint_wrappers=1:nokey=1', os.path.join(input_dir, input_filename)])
total_duration = float(video_info)
total_parts = int(total_duration / part_duration) + 1

# Split the video into parts
for i in range(total_parts):
    start_time = i * part_duration
    end_time = start_time + part_duration

    output_filename = output_filename_template.format(i+1)
    output_path = os.path.join(output_dir, output_filename)

    # Use ffmpeg to split the video
    subprocess.run(['ffmpeg', '-i', os.path.join(input_dir, input_filename), '-ss',
                   str(start_time), '-t', str(part_duration), '-c', 'copy', output_path])
