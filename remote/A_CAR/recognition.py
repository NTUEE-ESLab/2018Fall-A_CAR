import cv2
import sys
import numpy as np
import scipy.stats
import threading
from video_serial_server import video_serial_server

def make_template(width, height):
    center_x = width / 2.
    center_y = height / 2.
    r_x = width / 10.
    r_y = height / 10.
    template = np.ones((width, height), dtype = np.float32) * 255
    
    # using (1, 10, 24) instead of (1, 9, 25) get better results
    for x in range(width):
        for y in range(height):
            if (x - center_x) ** 2 / r_x ** 2 + (y - center_y) ** 2 / r_y ** 2 <= 1:
                template[x][y] = 0
            elif (x - center_x) ** 2 / r_x ** 2 + (y - center_y) ** 2 / r_y ** 2 >= 10 and\
                (x - center_x) ** 2 / r_x ** 2 + (y - center_y) ** 2 / r_y ** 2 <= 24:
                template[x][y] = 0

    return template

def match(picture, rect_width, rect_height, down_sample, strip, threshold = 115):
    picture = picture[::down_sample, ::down_sample]
    picture_width = picture.shape[1] // down_sample
    picture_height = picture.shape[0] // down_sample

    # make sure rect_width and rect_height are even number
    rect_width = rect_width // (down_sample * 2) * 2
    rect_height = rect_height // (down_sample * 2) * 2
    template = make_template(rect_width, rect_height)
    match_result = []
    
    # move window by 'strip' pixels in an iter
    for center_x in np.arange(int(rect_width / 2), picture_width - int(rect_width / 2),\
        strip):
        for center_y in np.arange(int(rect_height) / 2,\
            picture_height - int(rect_height / 2), int(round(rect_height / 5.))):
            # return all windows with losses under the threshold
            y1 = int(center_y - rect_height / 2)
            y2 = int(center_y + rect_height / 2)
            x1 = int(center_x - rect_width / 2)
            x2 = int(center_x + rect_width / 2)
            loss = np.mean(np.abs(template - picture[y1:y2, x1:x2]))
            if loss < threshold:
                x1 = x1 * down_sample
                y1 = y1 * down_sample
                x2 = x2 * down_sample
                y2 = y2 * down_sample
                match_result.append((x1, y1, x2, y2, loss))

    return match_result

def standarize(array):
    # standarizing and clipping to get a more contrastive image
    clip_bound = 0.5
    array = np.clip((scipy.stats.zscore(array.astype(np.uint8), axis = None) + clip_bound) / 2 / clip_bound * 255, 0, 255).astype(np.uint8)
    return array

class recognition():
    def __init__(self, video_capture, video_sender, cannon_controller):
        self.video_capture = video_capture
        self.video_sender = video_sender
        self.cannon_controller = cannon_controller
        # larger downsampling ratio for larger window sizes
        self.rect_widths = [20, 25, 30, 35, 40, 50, 60, 80, 100, 130, 160, 190, 220]
        self.rect_heights = [20, 25, 30, 35, 40, 50, 60, 80, 100, 130, 160, 190, 220]
        self.down_samples = [1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 5, 5, 5]
        self.thresholds = [95, 95, 95, 95, 95, 95, 95, 95, 95, 95, 95, 95, 95]
        self.enables = [True, True, True, True, True, True, True, True, True, True, True, True, True ]
        self.rect_widths.reverse()
        self.rect_heights.reverse()
        self.down_samples.reverse()
        self.thresholds.reverse()
        self.enables.reverse()

    def search(self):
        count = 0 # different count for different window size, downsampling ratio, etc
        candidates = []
        tracing_mode = False
        while True:
            if count == 0 and len(candidates) > 0:
                # entering the next stage if having found enough candidates
                self.trace(candidates)
                break

            ret, frame = self.video_capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = standarize(gray)

            match_rects = [] # possilble matching areas
    
            if self.enables[count]:
                match_rects = match(gray, self.rect_widths[count],\
                self.rect_heights[count], self.down_samples[count],\
                int(round(self.rect_widths[count] / 5)),\
                self.thresholds[count])

                if len(match_rects) == 0:
                    if self.thresholds[count] > 110:
                        self.enables[count] = False
                        # give up if not found even under large threshold
                    else:
                        self.thresholds[count] = self.thresholds[count] + 5
                        # increase threashold if not found
                elif len(match_rects) < 5:    
                    candidates = candidates + match_rects
                    # adding into candidates only when the matching results are reasonable
                else:
                    pass
                    # too many matched results lead to re-matching

                # visualization
                for x1, y1, x2, y2, _ in match_rects:
                    cv2.rectangle(gray, (x1, y1), (x2, y2), (0, 255, 255), 2)

            cv2.imshow('Video', gray)

            print(count, self.rect_widths[count], self.down_samples[count], self.thresholds[count], self.enables[count], len(match_rects))
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            count = (count + 1) % len(self.rect_heights)

            self.video_sender.data = frame[::5, ::5, ::-1]

    def trace(self, candidates):
        # tracing down particular area on the image with particular window size according to the result of self.search()
        count = 0
        best_loss = 255
        while candidates:
            ret, frame = self.video_capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = standarize(gray)
            match_rect = []

            x1, y1, x2, y2, loss = candidates[count]
            next_x1_list, next_y1_list, next_x2_list, next_y2_list = [], [], [], [] # possible new position of the matching windows since the video is moving, right?
            
            width = x2 - x1
            height = y2 - y1
            shift = 0.8 # search in a 2.6 * width x 2.6 * height area(2.6 = 1 + 0.8 * 2)
            best_loss_ = 255 # best_loss for the next iter
    
            subpicture = gray[int(y1 - shift * height):int(y2 + shift * height)\
                , int(x1 - shift * width): int(x2 + shift * width)]
            match_rects = match(subpicture, width, height, 1,\
                int(round(width / 10)), min(max(loss + 20, 85), 110))
            # precise matching: no downsampling, stride = 0.1 * width, and adaptive threshold
            # adding the loss + 20 term since we consider it may be a mis-matching if the error fluctuate severely

            for x1_, y1_, x2_, y2_, loss_ in match_rects:
                if loss_ < best_loss_:
                    best_loss_ = loss_
                y1_ = y1_ + int(y1 - shift * height)
                y2_ = y2_ + int(y1 - shift * height)
                x1_ = x1_ + int(x1 - shift * width)
                x2_ = x2_ + int(x1 - shift * width)
                next_x1_list.append(x1_)
                next_y1_list.append(y1_)
                next_x2_list.append(x2_)
                next_y2_list.append(y2_)
    
            print(candidates[count], count, len(candidates))
            if (len(match_rects) == 0 or best_loss_ > max(70, best_loss + 20))\
                and len(candidates) != 1:
                # remove the windows with nonideal loss from the candidates, except when the candidates has only one element remaining
                candidates.remove((x1, y1, x2, y2, loss))
            else:
                print(len(next_x1_list), best_loss_, best_loss)
                if len(next_x1_list) != 0:
                    # update the candidate list
                    next_x1 = np.mean(next_x1_list).astype(np.int)
                    next_y1 = np.mean(next_y1_list).astype(np.int)
                    next_x2 = np.mean(next_x2_list).astype(np.int)
                    next_y2 = np.mean(next_y2_list).astype(np.int)
                    candidates[count] = (next_x1, next_y1, next_x2, next_y2,\
                        best_loss_)
                else:
                    # if no matched result, retain original window and release the threshold(best_loss)
                    candidates[count] = (x1, y1, x2, y2, loss + 10)
                
                for x1_, y1_, x2_, y2_, loss_ in candidates:
                    cv2.rectangle(frame, (x1_, y1_), (x2_, y2_), (0, 255, 255), 5)
                best_x1, best_y1, best_x2, best_y2, best_loss = \
                    [min(item) for item in zip(*candidates)]
                count = count + 1

            count = count % len(candidates)
            cv2.imshow('Video', frame)

            self.video_sender.data = frame[::5, ::5, ::-1]
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if (best_x1 + best_x2) > frame.shape[1]:
                self.cannon_ctroller.target_orientation = -5
            else:
                self.cannon_ctroller.target_orientation = 5
            if (best_y1 + best_y2) > frame.shape[0]:
                self.cannon_ctroller.target_elevation = elevation + 5
            else:
                self.cannon_ctroller.target_orientation = elevation - 5

            if ((frame.shape[0] - (best_y1 + best_y2)) ** 2 +\
                (frame.shape[1] - (best_x1 + best_x2)) ** 2) < 1000:
                cannon_controller.fire()
                break
