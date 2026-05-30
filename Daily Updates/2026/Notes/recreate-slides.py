import re
import requests
from PIL import Image
from io import BytesIO
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import argparse
from pathlib import Path

def extract_image_urls(file_path, url_prefix="https://image.slidesharecdn.com"):
    """
    Read a file and extract all image URLs with the given prefix.
    Returns URLs in the order they appear in the text.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Regular expression to find URLs
        # This pattern matches http/https URLs that start with the prefix
        pattern = re.compile(r'(https?://[^\s<>"\'{}|\\^`\[\]]+)')
        all_urls = pattern.findall(content)
        
        # Filter URLs that start with the specified prefix
        filtered_urls = [url for url in all_urls if url.startswith(url_prefix)]
        
        return filtered_urls
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def download_image(url, output_dir="downloaded_slides"):
    """
    Download an image from a URL and save it locally.
    Returns the file path of the downloaded image.
    """
    try:
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Generate a filename from the URL
        # Extract the last part of the URL or use an index
        filename = url.split('/')[-1]
        if not filename or '.' not in filename:
            filename = f"slide_{hash(url) % 10000}.jpg"
        
        # Ensure the filename has an extension
        if not any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
            filename += '.jpg'
        
        filepath = os.path.join(output_dir, filename)
        
        # Download the image
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Save the image
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Downloaded: {filename}")
        return filepath
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed to download {url}: {e}")
        return None
    except Exception as e:
        print(f"✗ Error processing {url}: {e}")
        return None

def images_to_pdf(image_paths, output_pdf="slides_presentation.pdf"):
    """
    Combine multiple images into a single PDF file.
    Each image becomes one page in the PDF.
    """
    if not image_paths:
        print("No images to convert to PDF.")
        return False
    
    try:
        # Create PDF
        c = canvas.Canvas(output_pdf, pagesize=A4)
        page_width, page_height = A4
        
        for image_path in image_paths:
            if not os.path.exists(image_path):
                print(f"Warning: Image not found: {image_path}")
                continue
            
            try:
                # Open and get image dimensions
                img = Image.open(image_path)
                img_width, img_height = img.size
                
                # Calculate scaling to fit on A4 page while maintaining aspect ratio
                width_scale = page_width / img_width
                height_scale = page_height / img_height
                scale = min(width_scale, height_scale)
                
                # Calculate dimensions to fit on page
                scaled_width = img_width * scale
                scaled_height = img_height * scale
                
                # Center the image on the page
                x = (page_width - scaled_width) / 2
                y = (page_height - scaled_height) / 2
                
                # Draw the image
                img_reader = ImageReader(img)
                c.drawImage(img_reader, x, y, scaled_width, scaled_height)
                c.showPage()
                
                print(f"✓ Added to PDF: {os.path.basename(image_path)}")
                
            except Exception as e:
                print(f"✗ Error processing {image_path}: {e}")
                continue
        
        c.save()
        print(f"\n✓ PDF created successfully: {output_pdf}")
        return True
        
    except Exception as e:
        print(f"Error creating PDF: {e}")
        return False

def save_urls_to_file(urls, output_file="extracted_urls.txt"):
    """
    Save the extracted URLs to a text file.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for i, url in enumerate(urls, 1):
                f.write(f"{i}. {url}\n")
        print(f"✓ URLs saved to: {output_file}")
        return True
    except Exception as e:
        print(f"Error saving URLs: {e}")
        return False

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Extract image URLs from a file, download them, and create a PDF.')
    parser.add_argument('input_file', help='Path to the input text file')
    parser.add_argument('--prefix', default='https://image.slidesharecdn.com', 
                        help='URL prefix to filter images (default: https://image.slidesharecdn.com')
    parser.add_argument('--output-dir', default='downloaded_slides',
                        help='Directory to save downloaded images (default: downloaded_slides)')
    parser.add_argument('--output-pdf', default='slides_presentation.pdf',
                        help='Output PDF file name (default: slides_presentation.pdf)')
    parser.add_argument('--urls-file', default='extracted_urls.txt',
                        help='File to save extracted URLs (default: extracted_urls.txt)')
    parser.add_argument('--no-download', action='store_true',
                        help='Extract URLs but do not download images')
    parser.add_argument('--no-pdf', action='store_true',
                        help='Do not create PDF')
    
    args = parser.parse_args()
    
    # Step 1: Extract image URLs from the file
    print(f"Reading file: {args.input_file}")
    print(f"Looking for URLs with prefix: {args.prefix}")
    image_urls = extract_image_urls(args.input_file, args.prefix)
    
    if not image_urls:
        print("No image URLs found with the specified prefix.")
        return
    
    print(f"\nFound {len(image_urls)} image URLs:")
    for i, url in enumerate(image_urls[:5], 1):  # Show first 5 URLs
        print(f"  {i}. {url}")
    if len(image_urls) > 5:
        print(f"  ... and {len(image_urls) - 5} more")
    
    # Step 2: Save URLs to a text file
    save_urls_to_file(image_urls, args.urls_file)
    
    # Step 3: Download images (if not skipped)
    downloaded_images = []
    if not args.no_download:
        print(f"\nDownloading images to '{args.output_dir}'...")
        for i, url in enumerate(image_urls, 1):
            print(f"Downloading {i}/{len(image_urls)}: {url[:80]}...")
            image_path = download_image(url, args.output_dir)
            if image_path:
                downloaded_images.append(image_path)
        
        print(f"\nSuccessfully downloaded {len(downloaded_images)}/{len(image_urls)} images.")
        
        # Step 4: Create PDF (if not skipped and images were downloaded)
        if not args.no_pdf and downloaded_images:
            print(f"\nCreating PDF from {len(downloaded_images)} images...")
            images_to_pdf(downloaded_images, args.output_pdf)
        elif not args.no_pdf and not downloaded_images:
            print("\nNo images were downloaded, skipping PDF creation.")
    else:
        print("\nSkipped downloading images (--no-download flag used).")
    
    print("\n✅ Process completed!")
    print(f"   - Extracted URLs: {args.urls_file}")
    if not args.no_download:
        print(f"   - Downloaded images: {args.output_dir}/")
    if not args.no_pdf and not args.no_download:
        print(f"   - PDF presentation: {args.output_pdf}")

if __name__ == "__main__":
    main()
