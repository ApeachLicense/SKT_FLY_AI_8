import cv2
import numpy as np
import random
from collections import deque

# 1. 영상 크기 및 배경 설정
width, height = 640, 480
image = np.full((height, width, 3), 255, np.uint8) # 흰색 배경

# 시드 고정
random.seed(42)
shapes = [] 

def check_collision(new_shape, existing_shapes, margin=5):
    nx, ny, nr = new_shape
    for ex, ey, er in existing_shapes:
        dist = np.sqrt((nx - ex)**2 + (ny - ey)**2)
        if dist < (nr + er + margin): 
            return True
    return False

# 2. 랜덤 도형 생성 (기존 코드와 동일)
print("도형 생성 중...")
for i in range(50):
    cx = random.randint(50, width - 50)
    cy = random.randint(50, height - 50)
    # Red: (0, 0, 255), Green: (0, 255, 0), Blue: (255, 0, 0)
    color = random.choice([(0, 0, 255), (0, 255, 0), (255, 0, 0)])
    is_circle = random.choice([True, False])
    
    if is_circle:
        radius = random.randint(20, 60)
        if not check_collision((cx, cy, radius), shapes):
            cv2.circle(image, (cx, cy), radius, color, -1)
            shapes.append((cx, cy, radius))
    else: # 타원
        axis_x = random.randint(30, 60)
        axis_y = random.randint(20, 50)
        angle = random.randint(0, 180)
        max_radius = max(axis_x, axis_y)
        if not check_collision((cx, cy, max_radius), shapes):
            cv2.ellipse(image, (cx, cy), (axis_x, axis_y), angle, 0, 360, color, -1)
            shapes.append((cx, cy, max_radius))


# 3. BFS를 이용한 영역 탐색 및 사각형 그리기
print("탐색 시작 (BFS)...")
visited = np.zeros((height, width), dtype=bool) # 방문 여부 체크

# 결과 이미지 복사 (탐색 과정을 원본 위에 그리기 위해)
result_image = image.copy()

# 4방향 탐색 (상, 하, 좌, 우)
dx = [0, 0, -1, 1]
dy = [-1, 1, 0, 0]

for y in range(height):
    for x in range(width):
        # 방문하지 않았고, 흰색(255,255,255)이 아닌 픽셀 발견! (브루트포스)
        if not visited[y, x] and not np.array_equal(image[y, x], [255, 255, 255]):
            
            # BFS 시작
            q = deque([(x, y)])
            visited[y, x] = True
            
            # 영역의 최소/최대 좌표 찾기 (Bounding Box)
            min_x, max_x = x, x
            min_y, max_y = y, y
            
            # 픽셀 색상 수집 (대표 색상 판별용)
            color_sum = np.array([0, 0, 0], dtype=np.int32)
            pixel_count = 0
            
            while q:
                cx, cy = q.popleft()
                
                # 좌표 갱신 (박스 크기 조절)
                min_x = min(min_x, cx)
                max_x = max(max_x, cx)
                min_y = min(min_y, cy)
                max_y = max(max_y, cy)
                
                # 색상 누적
                color_sum += image[cy, cx]
                pixel_count += 1
                
                # 인접 픽셀 탐색
                for i in range(4):
                    nx, ny = cx + dx[i], cy + dy[i]
                    
                    if 0 <= nx < width and 0 <= ny < height:
                        if not visited[ny, nx] and not np.array_equal(image[ny, nx], [255, 255, 255]):
                            visited[ny, nx] = True
                            q.append((nx, ny))
            
            # 탐색 종료: 하나의 덩어리를 찾았음
            
            # 1. 평균 색상 계산
            avg_color = color_sum // pixel_count
            color_text = "Unknown"
            max_c_idx = np.argmax(avg_color) 
            if max_c_idx == 0: color_text = "Blue"
            elif max_c_idx == 1: color_text = "Green"
            elif max_c_idx == 2: color_text = "Red"

            # 2. 형상 판별 (이심률/종횡비 이용)
            # Box의 가로, 세로 길이 계산 (1을 더해야 실제 픽셀 수)
            box_w = max_x - min_x + 1
            box_h = max_y - min_y + 1
            
            # 종횡비(Aspect Ratio) 계산: 짧은변 / 긴변
            aspect_ratio = min(box_w, box_h) / max(box_w, box_h)
            
            # 원은 가로세로 비율이 거의 1.0에 가까움 (0.9 이상을 원으로 간주)
            if aspect_ratio >= 0.99:
                color_text = f"Circle ({color_text})"
                # 3. 사각형 박스 그리기 (원인 경우에만)
                cv2.rectangle(result_image, (min_x, min_y), (max_x, max_y), (0, 0, 0), 2)
                
                # 4. 정보 텍스트 출력
                cv2.putText(result_image, f"{color_text}", (min_x, min_y - 5), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            else:
                # 타원은 무시 (혹은 디버깅용으로 얇게 표시 가능)
                pass 

cv2.imshow("BFS Circle Detection", result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()