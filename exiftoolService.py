import json
import os
import shutil
import subprocess
from pathlib import Path
import platform


class ExifToolService:
    @staticmethod
    def _get_exiftool_command():
        if platform.system() == 'Windows':
            project_dir = Path(Path.resolve(Path(__file__))).parent
            local_candidates = [
                project_dir / 'exiftoll.exe',
                project_dir / 'exiftool.exe',
                project_dir / 'exiftool-13.58_64' / 'exiftool.exe',
            ]

            for candidate in local_candidates:
                if Path(candidate).is_file():
                    return candidate
        
        exiftool_cmd = shutil.which('exiftool') or shutil.which('exiftool.exe')
        if not exiftool_cmd:
            msg = (
                'ExifTool executable not found. Add exiftool.exe to the project folder, or install ExifTool and ensure it is in PATH.',
            )
            raise RuntimeError(msg)
        return exiftool_cmd

    @staticmethod
    def _build_windows_hidden_process_kwargs():
        if os.name != 'nt':
            return {}
        startup_info = subprocess.STARTUPINFO()
        startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        return {
            'startupinfo': startup_info,
            'creationflags': subprocess.CREATE_NO_WINDOW,
        }

    @staticmethod
    def _run_exiftool(args):
        command = [
            ExifToolService._get_exiftool_command(),
            '-charset',
            'filename=utf8',
            '-charset',
            'exif=utf8',
            *args,
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            encoding='utf-8',
            check=True,
            **ExifToolService._build_windows_hidden_process_kwargs(),
        )

        output = result.stdout
        if result.returncode != 0 or 'Error' in output:
            msg = f'ExifTool failed: {(result.stderr or output).strip()}'
            raise RuntimeError(msg)

        return output

    @staticmethod
    def read_metadata(image_path):
        output = ExifToolService._run_exiftool(
            [
                '-j',
                '-n',
                '-GPSLatitude',
                '-GPSLongitude',
                '-DateTimeOriginal',
                '-SubSecDateTimeOriginal',
                '-CreateDate',
                '-DateCreated',
                '-MediaCreateDate',
                '-TrackCreateDate',
                '-Keys:CreationDate',
                '-ModifyDate',
                '-FileCreateDate',
                '-FileModifyDate',
                '-City',
                '-Country',
                '-Country-PrimaryLocationName',
                '-Country-PrimaryLocationCode',
                '-XMP-iptcExt:LocationCreatedCountryCode',
                image_path,
            ],
        )

        parsed = json.loads(output)
        return parsed[0] if parsed else {}

    @staticmethod
    def write_gps_metadata(  # noqa: PLR0913
        image_path: str,
        latitude,
        longitude,
        city=None,
        country=None,
        country_code=None,
    ):
        latitude_ref = 'N' if latitude >= 0 else 'S'
        longitude_ref = 'E' if longitude >= 0 else 'W'

        args = [
            '-overwrite_original',
            f'-GPSLatitude={abs(latitude)}',
            f'-GPSLatitudeRef={latitude_ref}',
            f'-GPSLongitude={abs(longitude)}',
            f'-GPSLongitudeRef={longitude_ref}',
        ]

        if city and city != 'Unknown':
            args.extend(
                [
                    f'-IPTC:City={city}',
                    f'-XMP:City={city}',
                    f'-XMP-iptcExt:LocationCreatedCity={city}',
                ],
            )

        if country and country != 'Unknown':
            args.extend(
                [
                    f'-IPTC:Country-PrimaryLocationName={country}',
                    f'-XMP:Country={country}',
                    f'-XMP-iptcExt:LocationCreatedCountryName={country}',
                ],
            )

        if country_code:
            args.extend(
                [
                    f'-Country-PrimaryLocationCode={country_code}',
                    f'-IPTC:Country-PrimaryLocationCode={country_code}',
                    f'-XMP-iptcExt:LocationCreatedCountryCode={country_code}',
                ],
            )

        args.append(image_path)  # <-- append all paths
        ExifToolService._run_exiftool(args)

        """
        results = ExifToolService.read_metadata(["a.jpg", "b.jpg", "c.jpg"])
        for meta in results:
            print(meta["SourceFile"], meta.get("GPSLatitude"))
        """
