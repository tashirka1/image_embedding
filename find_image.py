from deepface import DeepFace
import psycopg
from datetime import datetime


from PIL import Image
import torch
from torchvision import models, transforms

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
    conn = psycopg.connect(dbname="default", user="default", password="default", host="localhost", port="5432")

    image = "images/001_fe3347c0.jpg"

    print("Image path: ", image)

    with conn.cursor() as cur:
        embeddings = DeepFace.represent(
            img_path = image, model_name = "Facenet512", enforce_detection=False, align=True
        )
        image_embedding = get_image_embedding(image).tolist()
        print("image_embedding")
        cur.execute(
            "SELECT file_name, image_embedding <-> %s::halfvec, image_embedding <=> %s::halfvec FROM items ORDER BY image_embedding <-> %s::halfvec LIMIT 5;",
            (image_embedding, image_embedding, image_embedding,)
        )
        rows = cur.fetchall()
        for row in rows:
            print(row)
        print("----- ")

        print("face_embedding")
        for embedding in embeddings:
            now = datetime.now()
            cur.execute(
                "SELECT file_name, face_embedding <-> %s::vector, face_embedding <=> %s::vector FROM items ORDER BY face_embedding <-> %s::vector LIMIT 5;",
                (embedding["embedding"], embedding["embedding"], embedding["embedding"],)
            )
            rows = cur.fetchall()
            for row in rows:
                print(row)
            print("----- ", datetime.now() - now)
main()
