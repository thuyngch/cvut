import os
import cv2
import argparse
from tqdm import tqdm


# ------------------------------------------------------------------------------
#  ArgumentParser
# ------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description=__file__)

parser.add_argument('video', type=str,
                    help="Path of the video input")

parser.add_argument('outdir', type=str,
                    help="Path of the output folder")

parser.add_argument('--start', type=int, default=0,
                    help="Start frame idx")

parser.add_argument('--stop', type=int, default=-1,
                    help="Stop frame idx")

parser.add_argument('--step', type=int, default=1,
                    help="Start frame idx")

parser.add_argument('--num', type=int, default=-1,
                    help="Maximum number of frames")

args = parser.parse_args()


# ------------------------------------------------------------------------------
#  Main execution
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print("\nStart extracting video \'{}\"...".format(args.video))
    cap = cv2.VideoCapture(args.video)
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    basename = os.path.basename(args.video)
    outdir = os.path.join(args.outdir, ".".join(basename.split('.')[:-1]))
    os.makedirs(outdir, exist_ok=True)

    start = args.start
    stop = args.stop if args.stop != -1 else num_frames
    step = args.step
    max_num_frames = args.num if args.num != -1 else num_frames

    num_get_frames = 0
    count_step = 0
    for idx in tqdm(range(num_frames), total=num_frames):
        status, frame = cap.read()
        if not status:
            break

        if idx < start:
            print(f"Skip frame {idx}")
            continue
        if idx >= stop:
            break
        if (count_step % step) != 0:
            count_step += 1
            continue

        outfile = os.path.join(outdir, 'frame_{:08d}.jpg'.format(idx+1))
        cv2.imwrite(outfile, frame)

        count_step += 1
        num_get_frames += 1
        if num_get_frames >= max_num_frames:
            print(f"Extract enough {max_num_frames} frames")
            break
    print("Extracted frames are saved at \'{}\"".format(outdir))
