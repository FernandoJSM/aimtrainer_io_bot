import pyautogui
import cv2
import numpy as np
from mss import mss
from matplotlib import pyplot as plt


def locate_target(image, target):
    target_height, target_width = target.shape[:2]

    res = cv2.matchTemplate(image=target, templ=image, method=cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(src=res)

    if max_val > 0.5:
        top_left = max_loc
        center = ((top_left[0] + target_width // 2), (top_left[1] + target_height // 2))

        # Plot target location
        # bottom_right = (top_left[0] + target_width, top_left[1] + target_height)
        # cv2.rectangle(img=image, pt1=top_left, pt2=bottom_right, color=(255, 0, 0), thickness=2)
        # plt.imshow(image, cmap="gray")
        # plt.show()

        return center
    else:
        return None


def run_bot(target, points, monitor):
    counter = 0
    sct = mss()
    while True:
        screenshot = cv2.cvtColor(
            src=np.array(sct.grab(monitor)), code=cv2.COLOR_RGB2GRAY
        )
        center = locate_target(image=screenshot, target=target)
        # print(center)
        if center is not None:
            pyautogui.click(center)
            counter += 1
            if counter == points:
                break


if __name__ == "__main__":
    # Setup:
    points = 50
    target_size = 20
    monitor = {"top": 0, "left": 0, "width": 1366, "height": 768}
    # --------------

    target = cv2.cvtColor(src=cv2.imread("target_35x35.png"), code=cv2.COLOR_RGB2GRAY)

    # Test code:
    # locate_target(
    #     image=cv2.cvtColor(
    #         src=cv2.imread(filename="test_screen.png"), code=cv2.COLOR_RGB2GRAY
    #     ),
    #     target=target,
    # )

    target = cv2.resize(
        src=target, dsize=(target_size, target_size), interpolation=cv2.INTER_AREA
    )

    run_bot(target=target, points=points, monitor=monitor)
