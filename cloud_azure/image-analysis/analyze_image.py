import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from PIL import Image, ImageDraw, ImageFont

def get_image_info():
    endpoint = os.getenv("AZURE_VISION_ENDPOINT")
    key = os.getenv("AZURE_VISION_KEY")
    if not endpoint or not key:
        raise SystemExit("Set AZURE_VISION_ENDPOINT and AZURE_VISION_KEY before analyzing an image.")
    credential = AzureKeyCredential(key)
    client = ImageAnalysisClient(endpoint=endpoint, credential=credential)
    file_path = input("분석할 이미지 파일 경로를 입력하세요: ")

    with open(file_path, 'rb') as image_file:
        this_image_data = image_file.read()

    result = client.analyze(
        image_data=this_image_data,
        visual_features=[
            VisualFeatures.TAGS,
            VisualFeatures.CAPTION,
            VisualFeatures.OBJECTS
        ]
    )

    print("이미지 캡션:")
    if result.caption:
        print(f" '{result.caption.text}': {result.caption.confidence:.4f}")

    print("\n이미지 태그:")
    if result.tags:
        for tag in result.tags.list:
            print(f" - {tag.name} (신뢰도: {tag.confidence:.4f})")

    image = Image.open(file_path)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    print("\n객체 감지:")
    if result.objects:
        for obj in result.objects.list:
            print(f" {obj.tags[0].name}: {obj.tags[0].confidence:.4f} at location {obj.bounding_box}")

            bbox = obj.bounding_box
            x, y, w, h = int(bbox.x), int(bbox.y), int(bbox.width), int(bbox.height)

            draw.rectangle([(x, y), (x + w, y + h)], outline="cyan", width=3)

            text = obj.tags[0].name
            text_bbox = draw.textbbox((x, y - 25), text, font=font)
            draw.rectangle(text_bbox, fill="cyan")
            draw.text((x, y - 25), text, fill="black", font=font)

    image.show()
    image.save("output.jpeg")

if __name__ == "__main__":
    get_image_info()
