import os
import numpy as np
from PIL import Image

def create_sample_images(directory="data", count=20, size=(512, 512)):
    """Create a set of sample images for testing."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    print(f"Generating {count} sample images in '{directory}'...")
    for i in range(count):
        # Generate a random colorful image
        data = np.random.randint(0, 256, (size[0], size[1], 3), dtype=np.uint8)
        # Add some patterns to make filters more visible
        # Draw a rectangle
        data[100:400, 100:400, 0] = 255 
        data[150:350, 150:350, 1] = 200
        
        img = Image.fromarray(data)
        img.save(os.path.join(directory, f"food_{i:03d}.jpg"))
    
    print("Sample images generated successfully.")

if __name__ == "__main__":
    create_sample_images()
