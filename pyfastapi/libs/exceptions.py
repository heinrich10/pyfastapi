class DomainError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class PersonNotFoundError(DomainError):
    def __init__(self, person_id: int):
        super().__init__(f"Person {person_id} not found", status_code=404)


class CountryNotFoundError(DomainError):
    def __init__(self, country_code: str):
        super().__init__(f"Country {country_code} not found", status_code=404)


class ContinentNotFoundError(DomainError):
    def __init__(self, continent_code: str):
        super().__init__(f"Continent {continent_code} not found", status_code=404)
