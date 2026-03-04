import numpy as np, cv2

ch0 = np.full((2, 4), 10, np.uint8) # 10으로 채운 행렬
ch1 = np.full((2, 4), 20, np.uint8) # 20으로 채운 행렬
ch2 = np.full((2, 4), 30, np.uint8) # 30으로 채운 행렬







print("[ch0] = \n", ch0)
print("[ch1] = \n", ch1)
print("[ch2] = \n", ch2)
print("[merge_bgr] = \n", merge_bgr)

for i, ch in enumerate(split_bgr):
    print(f"[split_bgr[{i}]] = \n{ch}")
