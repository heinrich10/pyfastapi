from sqlalchemy import select
from sqlalchemy.orm import Session
from unittest import TestCase

from pyfastapi.models import Country, Person
from pyfastapi.schemas import SortCountryEnum, QueryCountrySchema, SortPersonEnum, QueryPersonSchema
from pyfastapi.repositories import CountryRepository
from pyfastapi.repositories.base import extract_sort, extract_query

person_reference_sql = "SELECT persons.id, persons.last_name, persons.first_name \nFROM persons"

country_reference_sql = ("SELECT countries.code, countries.name, countries.phone, countries.symbol, countries.capital, "
                         "countries.currency, countries.alpha_3 \nFROM countries")


class TestBaseRepository(TestCase):
    repo: CountryRepository

    @classmethod
    def setUpClass(cls) -> None:
        cls.repo = CountryRepository(Session())

    def test_country(self) -> None:
        val = extract_sort(Country, SortCountryEnum, "name")(select(Country))
        print("val", val)

    def test_person(self) -> None:
        val = extract_sort(Person, SortPersonEnum, "id")(select(Person))
        print("person", val)


class TestCountryRepository(TestCase):
    def generate_from_sqlalchemy(self, sort_key_: str) -> str:
        stmt_ = extract_sort(Country, SortCountryEnum, sort_key_)(select(Country))
        return str(stmt_)

    def get_extract_query(self, q):
        return extract_query(Country, ["name"], q)(select(Country))

    def test_country_extract_sort_if_part_of_enum_asc(self) -> None:
        def generate_sql(sort_key_: str) -> str:
            return country_reference_sql + f" ORDER BY countries.{sort_key_} ASC"

        for element in SortCountryEnum:
            sort_key = element.value
            ans = generate_sql(sort_key)
            stmt = self.generate_from_sqlalchemy(sort_key)
            stmt_generated_with_plus = self.generate_from_sqlalchemy(f"+{sort_key}")

            assert str(stmt) == ans
            assert str(stmt_generated_with_plus) == ans

    def test_country_extract_sort_if_part_of_enum_desc(self) -> None:
        def generate_sql(sort_key_: str) -> str:
            return country_reference_sql + f" ORDER BY countries.{sort_key_} DESC"

        for element in SortCountryEnum:
            sort_key = element.value
            ans = generate_sql(sort_key)
            stmt = self.generate_from_sqlalchemy(f"-{sort_key}")

            assert str(stmt) == ans

    def test_country_extract_sort_if_not_part_of_enum(self) -> None:
        sort_key = "not_in_enum"
        ans = country_reference_sql
        stmt = self.generate_from_sqlalchemy(sort_key)
        assert str(stmt) == ans

    # extract query
    def test_country_extract_query1(self) -> None:
        ans = (country_reference_sql +
               " \nWHERE lower(countries.name) LIKE lower(:name_1) AND countries.continent_code = :continent_code_1")
        q = QueryCountrySchema.model_validate({"name": "name", "continent_code": "continent_code"})
        stmt = self.get_extract_query(q)
        assert str(stmt) == ans

    def test_country_extract_query2(self) -> None:
        ans = country_reference_sql + " \nWHERE countries.phone = :phone_1"
        q = QueryCountrySchema.model_validate({"phone": 1})
        stmt = self.get_extract_query(q)
        assert str(stmt) == ans

    def test_country_extract_query_not_in_enum(self) -> None:
        ans = country_reference_sql
        q = QueryCountrySchema.model_validate({"not_in_enum": "not_in_enum"})
        stmt = self.get_extract_query(q)
        assert str(stmt) == ans


class TestPersonRepository(TestCase):
    def generate_from_sqlalchemy(self, sort_key_: str) -> str:
        stmt_ = extract_sort(Person, SortPersonEnum, sort_key_)(select(Person))
        return str(stmt_)

    def get_extract_query(self, q):
        return extract_query(Person, ["first_name", "last_name"], q)(select(Person))

    # extract sort
    def test_person_extract_sort_if_part_of_enum_asc(self) -> None:
        def generate_sql(sort_key_: str) -> str:
            return person_reference_sql + f" ORDER BY persons.{sort_key_} ASC"

        for element in SortPersonEnum:
            sort_key = element.value
            ans = generate_sql(sort_key)
            stmt = self.generate_from_sqlalchemy(sort_key)
            stmt_generated_with_plus = self.generate_from_sqlalchemy(f"+{sort_key}")

            assert str(stmt) == ans
            assert str(stmt_generated_with_plus) == ans

    def test_person_extract_sort_if_part_of_enum_desc(self) -> None:
        def generate_sql(sort_key_: str) -> str:
            return person_reference_sql + f" ORDER BY persons.{sort_key_} DESC"

        for element in SortPersonEnum:
            sort_key = element.value
            ans = generate_sql(sort_key)
            stmt = self.generate_from_sqlalchemy(f"-{sort_key}")

            assert str(stmt) == ans

    def test_person_extract_sort_if_not_part_of_enum(self) -> None:
        sort_key = "not_in_enum"
        ans = person_reference_sql
        stmt = self.generate_from_sqlalchemy(sort_key)
        assert str(stmt) == ans

    # extract query
    def test_person_extract_query1(self) -> None:
        ans = (person_reference_sql +
               " \nWHERE lower(persons.last_name) LIKE lower(:last_name_1) AND "
               "lower(persons.first_name) LIKE lower(:first_name_1)")
        q = QueryPersonSchema.model_validate({"first_name": "ear", "last_name": "gre"})
        stmt = self.get_extract_query(q)
        assert str(stmt) == ans

    def test_person_extract_query2(self) -> None:
        ans = person_reference_sql + " \nWHERE persons.country_code = :country_code_1"
        q = QueryPersonSchema.model_validate({"country_code": "HK"})
        stmt = self.get_extract_query(q)
        assert str(stmt) == ans

    def test_person_extract_query_not_in_enum(self) -> None:
        ans = person_reference_sql
        q = QueryPersonSchema.model_validate({"not_in_enum": "not_in_enum"})
        stmt = self.get_extract_query(q)
        assert str(stmt) == ans
