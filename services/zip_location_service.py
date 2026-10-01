from data.zcta_repository import ZctaRepository


class ZipLocationService:
    def __init__(self):
        self.repository = ZctaRepository()

    def find(self, zip_code):
        return self.repository.get(zip_code)