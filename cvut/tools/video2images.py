import os
import cv2
import argparse
import numpy as np
from tqdm import tqdm


# ------------------------------------------------------------------------------
#  Main execution
# ------------------------------------------------------------------------------
def main():
    # ArgumentParser
    parser = argparse.ArgumentParser(
        description="Extract video to frames")

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

    parser.add_argument('--base', type=int, default=0,
                        help="Base 0/1")

    parser.add_argument('--txt-frames', type=str, default=None,
                        help="Txt file containing frames to extract")

    args = parser.parse_args()

    # get video
    print("\nStart extracting video \'{}\"...".format(args.video))
    cap = cv2.VideoCapture(args.video)
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # make outdir
    basename = os.path.basename(args.video)
    outdir = os.path.join(args.outdir, ".".join(basename.split('.')[:-1]))
    os.makedirs(outdir, exist_ok=True)

    # get attribs
    start = args.start
    stop = args.stop if args.stop != -1 else num_frames
    step = args.step
    max_num_frames = args.num if args.num != -1 else num_frames

    # txt frames
    selected_frames = None
    if args.txt_frames is not None:
        selected_frames = np.loadtxt(args.txt_frames, dtype=int)
        print(f"Selected frames: {selected_frames}")
        max_num_frames = num_frames

    # extract frames
    num_get_frames = 0
    count_step = 0
    for idx in tqdm(range(num_frames), total=num_frames):

        out_idx = idx if args.base == 0 else idx+1

        status, frame = cap.read()
        if not status:
            break

        if selected_frames is not None:
            if idx in selected_frames:
                outfile = os.path.join(outdir,
                                       'frame_{:08d}.jpg'.format(out_idx))
                cv2.imwrite(outfile, frame)
            continue

        if idx < start:
            print(f"Skip frame {idx}")
            continue
        if idx >= stop:
            break
        if (count_step % step) != 0:
            count_step += 1
            continue

        outfile = os.path.join(outdir, 'frame_{:08d}.jpg'.format(out_idx))
        cv2.imwrite(outfile, frame)

        count_step += 1
        num_get_frames += 1
        if num_get_frames >= max_num_frames:
            print(f"Extract enough {max_num_frames} frames")
            break
    print("Extracted frames are saved at \'{}\"".format(outdir))


if __name__ == "__main__":
    main()
