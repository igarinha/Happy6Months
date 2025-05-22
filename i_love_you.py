import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

def process_image(image_path, output_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Could not read {image_path}")
        return

    scale = 0.75
    img = cv2.resize(img, (int(img.shape[1] * scale), int(img.shape[0] * scale)))

    heart_positions = []
    penguin_positions = []
    mode = 1  # Default mode is drawing hearts

    def draw_heart(img, center, size=30, color=(0, 0, 255)):
        x, y = center
        pts = []

        for t in np.linspace(0, 2 * np.pi, 100):
            x_heart = size * 16 * (np.sin(t) ** 3)
            y_heart = -size * (13 * np.cos(t) - 5 * np.cos(2 * t) -
                               2 * np.cos(3 * t) - np.cos(4 * t))
            pts.append((int(x + x_heart), int(y + y_heart)))

        pts = np.array(pts, np.int32)
        cv2.fillPoly(img, [pts], color)

    def draw_penguin(img, center, size=30):
        x, y = center

        # Body
        body_color = (0, 0, 0)  # Black
        cv2.ellipse(img, (x, y), (size, int(size * 1.5)), 0, 0, 360, body_color, -1)

        # Belly
        belly_color = (255, 255, 255)  # White
        cv2.ellipse(img, (x, y + int(size * 0.3)), (int(size * 0.6), int(size)), 0, 0, 360, belly_color, -1)

        # Eyes
        eye_color = (255, 255, 255)  # White
        pupil_color = (0, 0, 0)  # Black
        eye_offset = int(size * 0.4)
        eye_radius = int(size * 0.2)
        pupil_radius = int(size * 0.1)

        cv2.circle(img, (x - eye_offset, y - int(size * 0.5)), eye_radius, eye_color, -1)
        cv2.circle(img, (x + eye_offset, y - int(size * 0.5)), eye_radius, eye_color, -1)
        cv2.circle(img, (x - eye_offset, y - int(size * 0.5)), pupil_radius, pupil_color, -1)
        cv2.circle(img, (x + eye_offset, y - int(size * 0.5)), pupil_radius, pupil_color, -1)

        # Beak
        beak_color = (0, 165, 255)  # Orange
        beak_pts = np.array([
            (x, y - int(size * 0.2)),
            (x - int(size * 0.2), y),
            (x + int(size * 0.2), y)
        ], np.int32)
        cv2.fillPoly(img, [beak_pts], beak_color)

        # Feet
        foot_color = (0, 165, 255)  # Orange
        foot_offset = int(size * 0.5)
        foot_size = int(size * 0.3)
        cv2.ellipse(img, (x - foot_offset, y + int(size * 1.5)), (foot_size, int(foot_size * 0.5)), 0, 0, 360, foot_color, -1)
        cv2.ellipse(img, (x + foot_offset, y + int(size * 1.5)), (foot_size, int(foot_size * 0.5)), 0, 0, 360, foot_color, -1)

    def on_mouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if mode == 1:
                heart_positions.append((x, y))
            elif mode == 2:
                penguin_positions.append((x, y))

    cv2.namedWindow('Add your love!')
    cv2.setMouseCallback('Add your love!', on_mouse)

    temp_img = img.copy()
    while True:
        display_img = temp_img.copy()
        for pos in heart_positions:
            draw_heart(display_img, pos, size=2.5)
        for pos in penguin_positions:
            draw_penguin(display_img, pos, size=30)

        cv2.putText(display_img, "Press 1: Hearts | Press 2: Penguins | Press S: Save", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 105, 180), 2)
        cv2.imshow('Add your love!', display_img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('1'):
            mode = 1
        elif key == ord('2'):
            mode = 2
        elif key == ord('s'):
            break

    cv2.destroyAllWindows()

    img_rgb = cv2.cvtColor(display_img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    draw = ImageDraw.Draw(pil_img)

    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    text = "Happy 6 Months Together! I love you Igarinha Gatinha bb!!!!!"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    width, height = pil_img.size
    text_x = (width - text_width) // 2
    text_y = height - text_height - 40

    draw.text((text_x, text_y), text, font=font, fill=(255, 105, 180))

    # Save
    final_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_path, final_img)

# Iterate through all images in the data/ directory
input_dir = 'data/'
output_dir = 'output/'

for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_edit.jpg")
        process_image(input_path, output_path)
