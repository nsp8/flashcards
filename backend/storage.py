from enum import StrEnum
from pathlib import Path
from dotenv import dotenv_values
import supabase

env_config = dotenv_values(".env")
url = env_config.get('SUPABASE_URL')
key = env_config.get('SUPABASE_KEY')
client = supabase.create_client(url, key)


class FileTypes(StrEnum):
    csv = "text/csv"
    json = "application/json"


def list_files_in_bucket(bucket_name: str) -> list:
    """List files in the Supabase bucket"""
    return client.storage.from_(bucket_name).list()


def list_files_in_folder(bucket_name: str, path: str) -> list:
    """List files in the Supabase bucket folder"""
    return client.storage.from_(bucket_name).list(path=path)


def upload_file_to_folder(
    local_file_path: Path,
    supabase_bucket: str,
    supabase_folder_path: str,
    file_type: FileTypes
):
    """Upload file to a folder in the Supabase bucket"""
    with open(local_file_path, "rb") as f:
        client.storage.from_(supabase_bucket).upload(
            file=f,
            path=f"{supabase_folder_path}/{local_file_path.name}",
            file_options={"content-type": file_type.value}
        )


def upsert_file(
    local_file_path: Path,
    supabase_bucket: str,
    supabase_folder_path: str,
    file_type: FileTypes
):
    with open(local_file_path, "rb") as f:
        client.storage.from_(supabase_bucket).update(
            file=f,
            path=f"{supabase_folder_path}/{local_file_path.name}",
            file_options={
                "content-type": file_type.value,
                "cache-control": "3600",
                "upsert": "true"
            }
        )


def move_file(bucket_name: str, source_path: str, dest_path: str):
    client.storage.from_(bucket_name).move(source_path, dest_path)
