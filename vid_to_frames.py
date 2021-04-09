import cv2
import os


def main():
    """
    Convert input video to downscaled, black and white jpeg images
    """
    folder = 'frames'
    try:
        os.mkdir(folder)
    except FileExistsError:
        pass

    vidcap = cv2.VideoCapture('Touhou_-_Bad_Apple.mp4')
    count = 0
    while True:
        success, image = vidcap.read()
        if not success:
            break
        thresh = 127
        img_binary = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)[1]
        small = cv2.resize(img_binary, (0, 0), fx=1/3,
                           fy=1/3, interpolation=cv2.INTER_AREA)
        cv2.imwrite(os.path.join(folder, "{:d}.jpg".format(count)), small)
        count += 1

    print("{} images are extacted in {}.".format(count, folder))


if __name__ == '__main__':
    main()
