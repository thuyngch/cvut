import cv2
import cvut
import argparse
from tqdm import tqdm


# ------------------------------------------------------------------------------
#  Main execution
# ------------------------------------------------------------------------------
def main():
    # ArgumentParser
    parser = argparse.ArgumentParser(
        description="Group frames to video")

    parser.add_argument('imgdir', type=str,
                        help="Path of the image directory")

    parser.add_argument('video', type=str,
                        help="Path of the output video")

    parser.add_argument('--fps', type=int, default=30,
                        help="Video FPS")

    args = parser.parse_args()

    # get images
    img_files = cvut.glob_imgs(args.imgdir)
    num_imgs = len(img_files)
    print(f"Number of imgs: {num_imgs}")

    # create video
    image = cv2.imread(img_files[0])
    size = (image.shape[1], image.shape[0])
    out = cvut.create_video(args.video, size, args.fps)

    for img_file in tqdm(img_files, total=len(img_files)):
        out.write(cv2.imread(img_file))

    print(f"Video is saved at {args.video}")


if __name__ == "__main__":
    main()
