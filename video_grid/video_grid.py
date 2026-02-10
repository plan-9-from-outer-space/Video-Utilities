
###################################################################################
# Take X input videos and create a single output video with an N x N grid layout.
###################################################################################
import cv2
import numpy as np
# import pyautogui

class VideoGrid:
    """Create an N x N output video grid layout from any number of input videos."""

    # var1 = 'junk'  # class variable shared by all instances

    def __init__ (self, input_paths, output_path):
        """Initialize the class instance."""
        self.input_paths = input_paths
        self.output_path = output_path

    def __str__ (self):
        return f"VideoGrid with {len(self.input_paths)} input videos and output path: {self.output_path}"

    def get_last_frame (self, cap):
        # Get the total number of frames in the video
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # Seek to the last frame
        cap.set (cv2.CAP_PROP_POS_FRAMES, total_frames - 1)
        # Read and return the last frame
        ret, frame = cap.read()
        return frame if ret else None

    def create_video_grid (self):
        
        input_paths = self.input_paths
        output_path = self.output_path

        # Update this code
        width = 640
        height = 360   # (640 / 360 = aspect ratio 16:9)
        fps = 30.0

        # if screen_size:
        #     screen_width, screen_height = screen_size
        # else:
        #     screen_width, screen_height = pyautogui.size()
        # print(f"Screen resolution: w = {screen_width} x h = {screen_height}")
        # Resolution: w = 2560 x h = 1440 (aspect ratio 16:9)
    
        # Calculate grid size based on the number of input videos
        num_videos = len(input_paths)
        grid_cols = int(np.ceil(np.sqrt(num_videos)))
        grid_rows = int(np.ceil(num_videos / grid_cols))
        print ("Output video:", grid_rows, "x", grid_cols, "grid")

        # Create the black video frame
        black_frame = np.zeros((height, width, 3), dtype=np.uint8)

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc (*'XVID')
        out = cv2.VideoWriter (output_path, fourcc, fps, (width * grid_cols, height * grid_rows))
        
        # Open the input video streams
        caps = [cv2.VideoCapture (path) for path in input_paths]
    
        # Get properties for the videos
        print ("Input video info:")
        for cap in caps:
            this_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            this_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            this_fps = cap.get(cv2.CAP_PROP_FPS)
            this_arr = this_height / this_width # aspect ratio reversed
            print(f"  Video properties: width={this_width}, height={this_height}, arr={this_arr}, fps={this_fps}")
            # Video properties: width=960, height=540, arr=0.5625, fps=25.0
            # Video properties: width=640, height=360, arr=0.5625, fps=50.0

        # This makes the video window resizable and allows the image to scale within it.
        # cv2.namedWindow("Video Display", cv2.WINDOW_NORMAL) 

        while True:
            frames = []
            return_values = []
            for cap in caps:
                ret, frame = cap.read()
                return_values.append(ret)
                if not ret:
                    # frames.append(black_frame) # .copy())
                    frames.append (self.get_last_frame (cap))
                else:
                    frames.append (frame)
            
            # If all videos have ended, break the loop
            if all (ret is False for ret in return_values):
                break
            
            # Resize the frames to ensure they fit in the grid
            frames = [cv2.resize (frame, (width, height)) for frame in frames]

            # Add a border around each frame
            border_color = (0, 0, 0)
            thickness = 5
            frames = [cv2.rectangle (frame, (0, 0), (width - 1, height - 1), border_color, thickness)
                        for frame in frames]

            # Stack the video frames in a N x N grid
            rows = []
            for i in range(grid_rows):
                row_frames = frames[i * grid_cols:(i + 1) * grid_cols]
                if len(row_frames) < grid_cols:
                    row_frames += [black_frame] * (grid_cols - len(row_frames))
                rows.append(np.hstack (row_frames))
            combined_frame = np.vstack (rows)
            
            # cv2.imshow("Video Display", combined_frame)
            # if cv2.waitKey(5000) & 0xFF == ord('q'):
            #     break

            # Write the completed frame to the output video
            out.write(combined_frame)
        
        for cap in caps:
            cap.release()
        out.release()
        cv2.destroyAllWindows()

