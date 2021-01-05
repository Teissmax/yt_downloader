import pytube
import argparse


# Print iterations progress
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()


def on_complete(stream, file_path):
    print(stream)
    print(file_path)


def on_progress(stream, chunk, remaining_bytes):
    # print("on_progress call")
    progress = total_size - remaining_bytes
    print_progress_bar(progress, total_size, length=50)


if __name__ == '__main__':
    menu_parser = argparse.ArgumentParser(description='Program to help downloading content on Youtube')

    menu_parser.add_argument("url", help="url of the video to download")
    menu_parser.add_argument("-t", "--type", help="choose to download the video or the audio",
                             choices=['audio', 'video'], default="audio")

    args = menu_parser.parse_args()

    video = pytube.YouTube(args.url)
    video.register_on_progress_callback(on_progress)
    video.register_on_complete_callback(on_complete)

    if args.type == 'audio':
        # line to download audio only and filtering out audio/webm mime_type
        stream_to_dl = video.streams.filter(only_audio=True, mime_type="audio/mp4").first()
        pass
    elif args.type == 'video':
        # line to download by tag (video+audio)
        stream_to_dl = video.streams.get_by_itag(22)
        pass
    else:
        print(f"what is this {args.type}")
        exit(0)

    total_size = stream_to_dl.filesize
    stream_to_dl.download(args.type)
