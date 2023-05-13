class MessagesConsts:
    LOGIN_ERROR = "Wrong username or password"
    ERROR_WHILE_UPLOADING_FILE_LOG = "error while uploading {filename}: {e}"
    ERROR_WHILE_UPLOADING_FILE = "error while uploading {filename}"
    ERROR_WHILE_UPLOADING_FILE_NO_SPACE = "error while uploading {filename} no space left"
    FILE_UPLOADED_SUCCESSFULLY = "successfully uploaded {filename}"
    FILE_UPLOAD_FAILED_SIZE_MISMATCH = "file upload failed size mismatch"
    FILE_UPLOAD_FAILED_SIZE_MISMATCH_LOG = "file upload '{filename}' failed size mismatch, {org_size} vs {saved_size}"
    FILE_REMOVED_SUCCESSFULLY = "File removed successfully"


class PaginationConsts:
    FILES_PER_PAGE = 25


class MediaConsts:
    BYTES_IN_MB = 1048576

    COMMON_VIDEO_EXTENSIONS = ["webm", "mp4"]
    COMMON_AUDIO_EXTENSIONS = ["aac", "mp3", "ogg"]
