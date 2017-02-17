import glob
import os
import cv2
import rsl.json_config as json_config

default_config = {
    'config_file_name': r'stitch_video_config.json',
    'source_dir_name': r'C:\sourcedir'
}


def stitch_video(config):
    for source_filename in glob.iglob(r'%s\*.mp4' % config['source_dir_name']):
        print('Reading: %s' % source_filename)
        source_fullpath = os.path.join(config['source_dir_name'], source_filename)
        cap = cv2.VideoCapture(source_fullpath)
        while True:
            (grabbed, current_frame) = cap.read()
            # if the frame could not be grabbed, then we have reached the end of the video
            if not grabbed:
                break
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
