import numpy as np
import cv2

from handleFrame import HandleFrame

import datetime
import json


class HandleVideo():
    def __init__(self):
        print("HandleVideo init...")
        self.HF= HandleFrame()

    def save(self, data):
        with open('output/test.json', 'w') as fout:
            json.dump(data, fout)


    def analysis(self, filename, show=False):
        vidcap = cv2.VideoCapture(filename)
        success, frame = vidcap.read()

        results= []
        cnt= 0
        while( success ):
            success, frame = vidcap.read()

            try: # for test frame no error
                cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            except:
                continue

            result= self.HF.pipeline(frame, show)
            results.append(result)

            cnt += 1
            print(cnt)

            if show:
                cv2.imshow('frame',frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("break....")
                    break

        print("video have number of freames: ", cnt)
        # print(results)
        self.save(results)

        vidcap.release()
        cv2.destroyAllWindows()

        return results

if __name__=="__main__":
    t1= datetime.datetime.now()

    filename= 'video/cuomo.webm' #990.87s
    filename= 'video/sri.webm' #990.87s

    HV= HandleVideo()
    results= HV.analysis(filename, True)
    print(results)


    t2= datetime.datetime.now()
    t21 = str( round((t2 - t1).total_seconds(), 2) ) + 's' 
    print(t21)

    print("done")

