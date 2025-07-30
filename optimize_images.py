#!/usr/bin/env python3
"""
Image optimization script for the portfolio website.
This script helps identify and optimize large images for better performance.
"""

import os
import subprocess
from pathlib import Path

def get_file_size_mb(file_path):
    """Get file size in MB."""
    return os.path.getsize(file_path) / (1024 * 1024)

def check_images():
    """Check image sizes and provide optimization recommendations."""
    static_dir = Path("static/img")
    
    print("🔍 Image Analysis Report")
    print("=" * 50)
    
    large_images = []
    total_size = 0
    
    for img_file in static_dir.rglob("*"):
        if img_file.is_file() and img_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
            size_mb = get_file_size_mb(img_file)
            total_size += size_mb
            
            if size_mb > 0.5:  # Images larger than 500KB
                large_images.append((img_file, size_mb))
    
    print(f"📊 Total images found: {len(list(static_dir.rglob('*.jpg')) + list(static_dir.rglob('*.png')))}")
    print(f"📊 Total size: {total_size:.2f} MB")
    print()
    
    if large_images:
        print("⚠️  Large images detected (recommended to optimize):")
        print("-" * 50)
        for img_path, size_mb in sorted(large_images, key=lambda x: x[1], reverse=True):
            print(f"📁 {img_path.name}: {size_mb:.2f} MB")
        
        print()
        print("💡 Optimization recommendations:")
        print("1. Convert to WebP format for better compression")
        print("2. Resize images to appropriate dimensions")
        print("3. Use progressive JPEG for better loading experience")
        print("4. Consider lazy loading for non-critical images")
        print()
        print("🛠️  To optimize images, you can use tools like:")
        print("- ImageOptim (Mac)")
        print("- TinyPNG (Online)")
        print("- Squoosh (Google)")
        print("- Pillow (Python library)")
    else:
        print("✅ All images are reasonably sized!")

def create_webp_versions():
    """Create WebP versions of images if Pillow is available."""
    try:
        from PIL import Image
        import glob
        
        static_dir = Path("static/img")
        webp_created = 0
        
        for img_path in static_dir.rglob("*"):
            if img_path.is_file() and img_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                webp_path = img_path.with_suffix('.webp')
                
                if not webp_path.exists():
                    try:
                        with Image.open(img_path) as img:
                            # Convert to RGB if necessary
                            if img.mode in ('RGBA', 'LA', 'P'):
                                img = img.convert('RGB')
                            
                            # Save as WebP with quality 85
                            img.save(webp_path, 'WEBP', quality=85, optimize=True)
                            webp_created += 1
                            print(f"✅ Created: {webp_path.name}")
                    except Exception as e:
                        print(f"❌ Failed to create WebP for {img_path.name}: {e}")
        
        if webp_created > 0:
            print(f"\n🎉 Created {webp_created} WebP versions!")
            print("💡 Update your HTML templates to use WebP with fallback:")
            print('<picture>')
            print('  <source srcset="image.webp" type="image/webp">')
            print('  <img src="image.jpg" alt="Description">')
            print('</picture>')
        else:
            print("ℹ️  No new WebP files created (they may already exist)")
            
    except ImportError:
        print("❌ Pillow not installed. Install with: pip install Pillow")
        print("💡 Then run this script again to create WebP versions.")

if __name__ == "__main__":
    print("🚀 Portfolio Image Optimization Tool")
    print("=" * 50)
    print()
    
    check_images()
    print()
    
    response = input("Would you like to create WebP versions of images? (y/n): ")
    if response.lower() in ['y', 'yes']:
        create_webp_versions()
    
    print("\n✨ Optimization analysis complete!") 