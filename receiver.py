# receiver.py
import time

import numpy as np

from methods.settings import *

port_in = 1235
port_out = 1236


def get_number_of_videos():
    print 'Receiver: Connecting with video_retriever.'
    s = socket.socket()
    s.bind((HOST, port_in))
    s.listen(1)
    while True:
        c, addr = s.accept()
        data = c.recv(1024)
        c.send('Received the message.')
        break
    s.close()
    c.close()
    return data


def get_frames():
    print 'Receiver: Connecting with server. Starting to collect all frames.'
    s = socket.socket()
    s.bind((HOST, port_in))
    s.listen(1)
    coll = []
    while True:
        c, addr = s.accept()
        data = c.recv(350000)
        if data == "stop":
            c.send('Stopping the server.')
            break
        else:
            test = np.fromstring(data, dtype=np.uint8)
            coll.append(test)
            c.send('Received the message.')
    print 'Receiver: All frames has been received.'
    s.close()
    c.close()
    return coll


def create_video(collection, path, fps, width, height, codec):
    print 'Receiver: Changing frames into video.'
    codec = cv2.VideoWriter_fourcc(*codec)
    out = cv2.VideoWriter('data/video/' + path, codec, fps, (width, height))
    for c in collection:
        frame = cv2.imdecode(c, 1)
        out.write(frame)
    out.release()
    print 'Receiver: Video has been created.'


def send_video():
    try:
        print 'Receiver: Connecting with statistics.'
        s = socket.socket()
        s.connect((HOST, port_out))
        s.send(PATH[i])
        s.close()
    except socket.error:
        print 'Receiver: Failed to connect with statistics. Will try again in 10 seconds.'
        time.sleep(10)
        send_video()


if __name__ == '__main__':
    print 'Receiver: Starting connections.'
    counter = int(float(get_number_of_videos()))
    for i in range(counter):
        frames = get_frames()
        create_video(frames, PATH[i], FPS[i], WIDTH[i], HEIGHT[i], CODEC[i])
        send_video()
    print 'Receiver: All data has been sent. Closing connections.'
