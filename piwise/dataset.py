import numpy as np
import os

from PIL import Image
from torch.utils import data

EXTENSIONS = ['.jpg', '.png']

def load_image(file):
    return Image.open(file).convert('RGB')

def is_image(filename):
    return any(filename.endswith(ext) for ext in EXTENSIONS)

def image_path(root, basename, extension):
    return os.path.join(root, f'{basename}{extension}')

def image_basename(filename):
    return os.path.basename(os.path.splitext(filename)[0])

class VOC2012(data.Dataset):

    def __init__(self, root, input_transform=None, target_transform=None):
        self.images_root = os.path.join(root, 'images')
        self.classes_root = os.path.join(root, 'classes')

        self.filenames = [image_basename(f)
            for f in os.listdir(self.classes_root) if is_image(f)]
        self.filenames.sort()

        self.input_transform = input_transform
        self.target_transform = target_transform

    def __getitem__(self, index):
        filename = self.filenames[index]

        with open(image_path(self.images_root, filename, '.jpg'), 'rb') as f:
            image = load_image(f)
        with open(image_path(self.classes_root, filename, '.png'), 'rb') as f:
            classes = load_image(f)

        if self.input_transform is not None:
            image = self.input_transform(image)
        if self.target_transform is not None:
            classes = self.target_transform(classes)

        return image, classes

    def __len__(self):
        return len(self.filenames)