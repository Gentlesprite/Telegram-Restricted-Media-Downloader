# coding=UTF-8
# Author:from Internet
# Software:PyCharm
# Time:2023/11/12 20:52:12
# File:pyrogram_extension.py
from io import BytesIO
from pyrogram.file_id import (
    FILE_REFERENCE_FLAG,
    PHOTO_TYPES,
    WEB_LOCATION_FLAG,
    FileType,
    b64_decode,
    rle_decode,
)
import struct
from module import mimetypes
from module import Optional
from module.enum_define import Extension

_mimetypes = mimetypes.MimeTypes()


def get_extension(file_id: str, mime_type: str, dot: bool = True) -> str:
    """Get extension
    更多扩展见:http://www.iana.org/assignments/media-types/media-types.xhtml
    """

    if not file_id:
        if dot:
            return ".unknown"
        return "unknown"

    file_type = _get_file_type(file_id)

    guessed_extension = _guess_extension(mime_type)

    if file_type in PHOTO_TYPES:
        extension = Extension.photo.get(mime_type, 'jpg')
    elif file_type == FileType.VOICE:
        extension = guessed_extension or 'ogg'
    elif file_type in (FileType.VIDEO, FileType.ANIMATION, FileType.VIDEO_NOTE):
        extension = guessed_extension or Extension.video.get(mime_type, 'mp4')
    elif file_type == FileType.DOCUMENT:
        if 'video' in mime_type:
            extension = guessed_extension or Extension.video.get(mime_type, 'mp4')
        elif 'image' in mime_type:
            extension = guessed_extension or Extension.photo.get(mime_type, 'jpg')  # v1.2.8 修复获取图片格式时,实际指向为视频字典的错误。
        else:
            extension = guessed_extension or 'zip'
    elif file_type == FileType.STICKER:
        extension = guessed_extension or 'webp'
    elif file_type == FileType.AUDIO:
        extension = guessed_extension or 'mp3'
    else:
        extension = 'unknown'

    if dot:
        extension = '.' + extension
    return extension


def _guess_extension(mime_type: str) -> Optional[str]:
    """Guess the file extension from a MIME type return without dot if extension isn't None."""
    extension = mimetypes.guess_extension(mime_type, strict=True)
    return extension[1:] if extension and extension.startswith('.') else extension


def _get_file_type(file_id: str):
    """Get file type"""
    decoded = rle_decode(b64_decode(file_id))

    # File id versioning. Major versions lower than 4 don't have a minor version
    major = decoded[-1]

    if major < 4:
        buffer = BytesIO(decoded[:-1])
    else:
        buffer = BytesIO(decoded[:-2])

    file_type, _ = struct.unpack("<ii", buffer.read(8))

    file_type &= ~WEB_LOCATION_FLAG
    file_type &= ~FILE_REFERENCE_FLAG

    try:
        file_type = FileType(file_type)
    except ValueError as exc:
        raise ValueError(f"Unknown file_type {file_type} of file_id {file_id}") from exc

    return file_type
