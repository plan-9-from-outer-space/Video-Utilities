from glob import glob
from video_grid import VideoGrid

if __name__ == "__main__":
    # Use glob to create a list of the desired input videos
    input_paths = \
        glob("resources/*.mp4") + \
        glob("resources/*.avi") 
    print("Input Paths =", input_paths)

    num_videos = len(input_paths)
    output_path = f"outputs/video_grid_{num_videos}.avi"

    # Create the video grid
    vg = VideoGrid (input_paths, output_path)
    vg.create_video_grid ()
