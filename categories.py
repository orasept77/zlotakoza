from typing import Dict, List, NamedTuple

import db


class Category(NamedTuple):
    codename: str
    name: str
    is_dzieny_dochod: bool
    aliases: List[str]


class Categories:
    def __init__(self):
        self._categories = self._load_categories()

    def _load_categories(self) -> List[Category]:
        categories = db.fetchall(
            "category", "codename name is_dzieny_dochod aliases".split()
        )
        categories = self._fill_aliases(categories)
        return categories

    @staticmethod
    def _fill_aliases(categories: List[Dict]) -> List[Category]:

        categories_result = []
        for index, category in enumerate(categories):
            aliases = category["aliases"].split(",")
            aliases = list(filter(None, map(str.strip, aliases)))
            aliases.append(category["codename"])
            aliases.append(category["name"])
            categories_result.append(Category(
                codename=category['codename'],
                name=category['name'],
                is_dzieny_dochod=category['is_dzieny_dochod'],
                aliases=aliases
            ))
        return categories_result

    def get_all_categories(self) -> List[Category]:

        return self._categories

    def get_category(self, category_name: str) -> Category:
        finded = None
        other_category = None
        for category in self._categories:
            if category.codename == "other":
                other_category = category
            for alias in category.aliases:
                if category_name in alias:
                    finded = category
        if not finded:
            finded = other_category
        return finded
