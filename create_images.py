from deepface import DeepFace
import psycopg

from PIL import Image
import torch
from torchvision import models, transforms
from pathlib import Path

model = models.resnet50(pretrained=True)
model.eval()  # Set to evaluation mode

# Remove the final classification layer to get embeddings
model = torch.nn.Sequential(*list(model.children())[:-1])

# Image preprocessing
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


def get_image_embedding(image_path):
    image = Image.open(image_path).convert("RGB")
    image_tensor = preprocess(image).unsqueeze(0)
    with torch.no_grad():
        embedding = model(image_tensor)
    return embedding.squeeze().numpy()


def main():
    path = Path("./images")
    images = [f"./images/{f.name}" for f in path.iterdir() if f.is_file()]

    conn = psycopg.connect(dbname="default", user="default", password="default", host="localhost", port="5432")

    for image in images:
        with conn.cursor() as cur:
            embeddings = DeepFace.represent(
                img_path = image, model_name = "Facenet512", enforce_detection=False, align=True
            )
            image_embedding = get_image_embedding(image).tolist()
            for i, embedding in enumerate(embeddings):
                print(image, i, len(embedding["embedding"]))
                cur.execute("INSERT INTO items (file_name, face, face_embedding, image_embedding) VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING", (image, i, embedding["embedding"], image_embedding))

    conn.commit()

main()
