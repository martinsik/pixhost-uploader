# pixhost-uploader

Unofficial Python 3.2+ upload client for pixhost.org image sharing website.

## Usage

```python
import pixhostuploader as pixhost

uploaded = pixhost.upload('image.jpg')

print(uploaded)
```

Uploader returns 3 URLs for each image: thumbnail, full size image and a its page on pixhost.org.

```python
{
    'thumb_image': '...',
    'full_size_image': '...',
    'page_url': '...',
}
```

You can also upload multiple images at once.

```python
images = [
    'image.jpg',
    'another_image.jpg',
]
uploaded = pixhost.upload(images)
```

Uploader then returns a `list` of URLs for each uploaded image.

```python
[
    {
        'thumb_image': '...',
        'full_size_image': '...',
        'page_url': '...',
    }, {
        'thumb_image': '...',
        'full_size_image': '...',
        'page_url': '...',
    }
]
```

Maximum image size on pixhost.org is 10 MB so if you try to upload a larger file the upload function throws `TooLargeImageFormat` exception.  
Also in case the upload fails for some reason (upload page doesn't return `200` code) `UploadFailed` is thrown.
