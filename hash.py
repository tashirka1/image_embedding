from PIL import Image
import imagehash

images = [
    "images/girl1.jpeg",
    "images/girl2.jpeg",
    "images/girl3.jpeg",
    "images/girl4.jpeg",
    "images/girl5.jpeg",
    "images/girl6.jpeg",
    "images/girl7.jpeg",
    "images/susanna1.jpeg",
    "images/susanna2.jpeg",
    "images/susanna3.jpeg",
    "images/susanna4.jpeg",
    "images/susanna5.jpeg",
    "images/susanna6.jpeg",
    "images/susanna7.jpeg",
    "images/susanna8.jpeg",
    "images/susanna9.jpeg",
    "images/susanna10.jpeg",
    "images/matt-daymon.jpeg",
    "images/matt-daymon-2.jpg",
    "images/matt-daymon-3.jpg",
    "images/garik-harlamov.jpg",
    "images/garik-harlamov-2.jpg",
    "images/kimoriiii-1.jpeg",
    "images/kimoriiii-2.jpeg",
    "images/kimoriiii-3.jpeg",
    "images/kimoriiii-4.jpeg",
    "images/kimoriiii-5.jpeg",
    "images/kimoriiii-6.jpeg",
    "images/kimoriiii-7.jpeg",
]


hash = imagehash.average_hash(Image.open('images/susanna1.jpeg'))

for image in images:
    otherhash = imagehash.average_hash(Image.open(image))
    print(f"{image}: ", hash - otherhash)
