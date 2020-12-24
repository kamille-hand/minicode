import cv2


def playVideoByFrame(videoPath):
    cap = cv2.VideoCapture(videoPath)
    while(cap.isOpened()):
        ret, frame = cap.read()
        cv2.imshow("test", frame)
        if cv2.waitKey(delay=30) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    playVideoByFrame("D:/FFOutput/VID20201201180114.mp4")
