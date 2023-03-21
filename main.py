import cv2
import time
import os
import win32gui
import win32con


def create_footage_directory():
    try:
        os.mkdir('footages')
    except FileExistsError:
        pass


def minimize_window():
    window = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(window, win32con.SW_MINIMIZE)


def setup_camera():
    camera = cv2.VideoCapture(0)
    camera.set(3, 640)  # Set camera resolution
    camera.set(4, 480)
    width = camera.get(3)
    height = camera.get(4)
    print("Video resolution is set to: ", width, 'X', height)
    print("--Help:  1. press esc key to exit CCTV\n2. press m to minimize window.")
    return camera


def record_video(camera):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    date_time = time.strftime("recording %H-%M-%d-%m-%y")  # Set current time as video name
    output = cv2.VideoWriter(f'footages/{date_time}.mp4', fourcc, 20.0, (640, 480))

    while camera.isOpened():
        check, frame = camera.read()
        if check:
            frame = cv2.flip(frame, 1)

            # Show recording time
            t = time.ctime()
            cv2.rectangle(frame, (5, 5, 100, 20), (255, 255, 255), cv2.FILLED)
            cv2.putText(frame, "Camera 1", (20, 20),
                        cv2.FONT_HERSHEY_DUPLEX, 0.5, (5, 5, 5), 2)
            cv2.putText(frame, t, (420, 460),
                        cv2.FONT_HERSHEY_DUPLEX, 0.5, (5, 5, 5), 1)

            cv2.imshow('CCTV camera', frame)
            output.write(frame)

            # Close window when user presses Esc key
            key = cv2.waitKey(1)
            if key == 27:
                print("Video footage saved in 'footages' directory.\nStay safe & secure!")
                break
            # Minimize window when user presses M key
            elif key == ord('m'):
                minimize_window()
        else:
            print("Cannot open this camera. Please select another camera or check its configuration.")
            break

    camera.release()
    output.release()
    cv2.destroyAllWindows()


def main():
    print("*" * 80 + "\n" + " " * 30 + "Welcome to CCTV software\n" + "*" * 80)
    ask = int(input('Do you want to start CCTV?\n1. Yes\n2. No\n>>> '))
    if ask == 1:
        create_footage_directory()
        camera = setup_camera()
        record_video(camera)
    elif ask == 2:
        print("Goodbye! Stay safe & secure!")
        exit()


if __name__ == '__main__':
    main()
