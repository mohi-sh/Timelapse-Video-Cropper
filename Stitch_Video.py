import glob
import os
import cv2
from datetime import datetime
import rsl.json_config as json_config

default_config = {
    'config_file_name': r'stitch_video_config.json',
    'fourcc_text': 'XVID',
    'source_dir_name': r'C:\source_dir'
}


def get_cap_prop_size(cap):
    return int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


def mp4_file_iterator(config):
    return glob.iglob(r'%s\*.mp4' % config['source_dir_name'])

def stitch_video(config):
    print('Stitching all MP4 files in directory:\n\t%s' % config['source_dir_name'])
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target_filename = '%s_stitched.avi' % timestamp
    target_fullpath = os.path.join(config['source_dir_name'], target_filename)
    fourcc = cv2.VideoWriter_fourcc(*config['fourcc_text'])
    video = None
    file_list = mp4_file_iterator(config)
    n = 0
    for f in file_list:
        n += 1
    print('Found %d MP4 files.' % n)
    print('Writing stitched video to:\n\t%s' % target_fullpath)
    file_list = mp4_file_iterator(config)
    i = 0
    for source_filename in file_list:
        i += 1
        print('%d/%d] %s' % (i, n, source_filename))
        source_fullpath = os.path.join(config['source_dir_name'], source_filename)
        cap = cv2.VideoCapture(source_fullpath)
        if video is None:
            original_fps = cap.get(cv2.CAP_PROP_FPS)
            frame_width, frame_height = get_cap_prop_size(cap)
            video = cv2.VideoWriter(target_fullpath, fourcc, original_fps, (frame_width, frame_height), True)
        while True:
            (grabbed, current_frame) = cap.read()
            # if the frame could not be grabbed, then we have reached the end of the video
            if not grabbed:
                break
            video.write(current_frame)
            cv2.imshow('Source Video', current_frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                raise KeyboardInterrupt


def main():
    config_file_name = default_config['config_file_name']

    try:
        config = json_config.load(config_file_name)
        if not os.path.isdir(config['source_dir_name']):
            print('source_dir_name is not a directory: \n\t%s' % config['source_dir_name'])
            json_config.print_config(config)
            return 1
        json_config.normalize(config, default_config)
    except FileNotFoundError:
        json_config.create_default(default_config)

    stitch_video(config)


if __name__ == '__main__':
    try:
        main()
        print('\n[Normal Exit]')
    except KeyboardInterrupt:
        print('\n[User Exit]')
    except SystemExit:
        print('\n[System Exit]')
