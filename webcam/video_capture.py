#!/usr/bin/python3

import sys
import getopt

import cv2

def usage():
    print("Usage : {0}".format(sys.argv[0]))
        
def main():
    ret = 0

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvo:",
                [
					"help",
                    "version",
                    "logfile="
                ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)
	
    logfile = None
	
    for opt, arg in opts:
        if opt == "-v":
            usage()
            sys.exit(0)
        elif opt in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif opt in ("-l", "--logfile"):
            logfile = arg
        else:
            assert False, "unknown option"
	
    if ret != 0:
        sys.exit(1)

    if logfile :
        log = open(logfile, mode='w', encoding='utf-8')
	
    for filepath in args:
        print("arg : {0}".format(filepath))

    print('cv2 version {0}'.format(cv2.__version__))

    cap = cv2.VideoCapture(0)
    ret = cap.get(cv2.CAP_PROP_CONVERT_RGB)

    if not cap.isOpened():
        print('can not open video capture')
        sys.exit(1)

    avg = None

    while 1:
        ret, frame = cap.read()
        #frame = cv2.resize(frame,
        #    (int(frame.shape[1]*0.7), int(frame.shape[0]*0.7)))

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if avg is None :
            avg = gray.copy().astype("float")
            continue

        cv2.accumulateWeighted(gray, avg, 0.6)
        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

        thresh = cv2.threshold(frameDelta, 3, 255, cv2.THRESH_BINARY)[1]
        image, contours, hierarchy = cv2.findContours(
                thresh.copy(),
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

        frame = cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
        cv2.imshow('frame', frame)

        key = cv2.waitKey(1)

        # check escape key
        if key == 27 :
            break

    cap.release()

    cv2.destroyAllWindows()

    if logfile :
        log.close()
	
if __name__ == "__main__":
	main()
