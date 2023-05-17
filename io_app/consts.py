class MessagesConsts:
    LOGIN_ERROR = "Wrong username or password"
    ERROR_WHILE_UPLOADING_FILE_LOG = "error while uploading {filename}: {e}"
    ERROR_WHILE_UPLOADING_FILE = "error while uploading {filename}"
    ERROR_WHILE_UPLOADING_FILE_NO_SPACE = "error while uploading {filename} no space left"
    ERROR_WHILE_UPLOADING_FILE_EXISTS = "error while uploading {filename} file with the same name already exists"
    FILE_UPLOADED_SUCCESSFULLY = "successfully uploaded {filename}"
    FILE_UPLOAD_FAILED_SIZE_MISMATCH = "file upload failed size mismatch"
    FILE_UPLOAD_FAILED_SIZE_MISMATCH_LOG = "file upload '{filename}' failed size mismatch, {org_size} vs {saved_size}"
    FILE_REMOVED_SUCCESSFULLY = "File removed successfully"
    DIRECTORY_REMOVED_SUCCESSFULLY = "Directory removed successfully"
    DIRECTORY_EXISTS = "Directory exists"
    DIRECTORY_DOESNT_EXIST = "Directory doesn't exist"
    DIRECTORY_ADDED = "Directory added successfully"
    DIRECTORY_CHANGED = "Directory changed"
    FILE_DOESNT_EXIST = "File doesn't exist"
    UPDATED_DIRECTORY_FILES = "Successfully updated {files_count} files"
    USER_DOESNT_EXIST = "User doesn't exist"
    CANT_SHARE_DIRECTORY_TO_SELF = "Can't share directory to self"
    SHARED_TO_USER = "Shared {obj_name} to {username}"
    ERROR_WHILE_SHARING_DIRECTORY_TO_USER = "Error while sharing directory to user"
    DIRECTORY_ALREADY_SHARED_TO_USER = "Directory already shared to user"
    REMOVE_SHARED_TO_USER = "Removed {obj_name} sharing to {username}"
    DIRECTORY_NOT_SHARED_TO_USER = "Directory not shared to user"


class PaginationConsts:
    FILES_PER_PAGE = 25


class MediaConsts:
    BYTES_IN_MB = 1048576

    COMMON_VIDEO_EXTENSIONS = ["webm", "mp4"]
    COMMON_AUDIO_EXTENSIONS = ["aac", "mp3", "ogg"]
