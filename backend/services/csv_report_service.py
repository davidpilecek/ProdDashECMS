from pathlib import Path


class CsvService:

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

    def get_production_csv(
        self,
        month: int,
        year: int,
    ) -> Path:

        filename = (
            f"{month:02d}{year}_PROD_SEGMENT.csv"
        )

        file_path = self.data_dir / filename

        if not file_path.is_file():
            raise FileNotFoundError(filename)

        return file_path