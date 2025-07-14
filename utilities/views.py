
from django.shortcuts import render, HttpResponse
from pdf2image import convert_from_path
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings
import os
import zipfile
from io import BytesIO

# dev_urls import
from django.urls import get_resolver, URLPattern, URLResolver, reverse, NoReverseMatch
from collections import defaultdict

def pdf_to_image(request):
    if request.method == 'POST' and request.FILES.get('pdf'):
        pdf = request.FILES['pdf']
        output_dir = os.path.join(settings.MEDIA_ROOT, 'images')
        os.makedirs(output_dir, exist_ok=True)

        try:
            # Save PDF temporarily
            pdf_path = os.path.join(output_dir, pdf.name)
            with open(pdf_path, 'wb') as file:
                for chunk in pdf.chunks():
                    file.write(chunk)

            # Get the channel layer
            channel_layer = get_channel_layer()
            group_name = 'conversion_progress'

            # Convert PDF to images
            images = convert_from_path(pdf_path, dpi=300, fmt='png')

            image_urls = []
            zip_buffer = BytesIO()
            zip_filename = os.path.join(output_dir, 'converted_images.zip')

            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for i, image in enumerate(images):
                    image_name = f"page_{i + 1}.png"
                    image_path = os.path.join(output_dir, image_name)
                    image.save(image_path, 'PNG')

                    # Add to ZIP file
                    zip_file.write(image_path, image_name)

                    # Send progress update to WebSocket
                    progress = int(((i + 1) / len(images)) * 100)
                    async_to_sync(channel_layer.group_send)(
                        group_name,
                        {
                            'type': 'send_progress',
                            'progress': progress,
                            'message': f'Processed page {i + 1} of {len(images)}'
                        }
                    )

                    # Store the relative URL for single image download
                    image_url = f"/media/images/{image_name}"
                    image_urls.append(image_url)

            # Save the ZIP file
            with open(zip_filename, 'wb') as f:
                f.write(zip_buffer.getvalue())

            zip_url = f"/media/images/converted_images.zip"
            return render(request, 'utilitie/pdf_to_image.html', {'images': image_urls, 'zip_url': zip_url})

        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)
            # return render(request, 'utilitie/spdf_to_image.html', {'error': str(e)})

    return render(request, 'utilitie/pdf_to_image.html')




def list_urls_by_app():
    resolver = get_resolver()
    url_patterns = resolver.url_patterns

    def extract(patterns, app_name=None):
        urls = defaultdict(list)
        for p in patterns:
            if isinstance(p, URLPattern):
                if p.name:
                    try:
                        url = reverse(p.name)
                        app = app_name or p.callback.__module__.split('.')[0]
                        urls[app].append((p.name, url))
                    except NoReverseMatch:
                        pass
            elif isinstance(p, URLResolver):
                sub_urls = extract(p.url_patterns, p.app_name or app_name)
                for k, v in sub_urls.items():
                    urls[k].extend(v)
        return urls

    return extract(url_patterns)

def dev_urls(request):

    return render(request, 'tools-dashboard.html',)