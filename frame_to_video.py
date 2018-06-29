# Program To Read video
# and Extract Frames
import cv2
import datetime
interval = 1000

# Function to extract frames
def FrameCapture(path):

    # Path to video file
    vidObj = cv2.VideoCapture(path)

    # Used as counter variable
    count = 0

    # checks whether frames were extracted
    success = 1
    image_saved = 1
    while success:

        # vidObj object calls read
        # function extract frames
        success, image = vidObj.read()
        date_and_time = datetime.datetime.now()
        d_t = date_and_time.isoformat()
        d_t = str(d_t)
        d_t = d_t.replace(".", "")
        d_t = d_t.replace(":", "")
        d_t = d_t.replace("-", "")
        frame_name = save_path + "men_t" + "_"+ d_t+".jpg"
        count_to_save_image = interval * image_saved

        # Saves the frames with frame-count
        if (count == count_to_save_image ):
            print "count_to_save_image--------->>>>>",count_to_save_image
            image_saved = image_saved + 1
            print "image_saved",image_saved
            cv2.imwrite(frame_name, image)

        count += 1
        # print "count ---->>>>",count

# Driver Code
if __name__ == '__main__':
    save_path = "/video/image_save/"
    # Calling the function
    FrameCapture("data/video/1.mp4")
