import re
import typing as t

import sqlalchemy as sa

from app.extensions import db
from app.models.orm.lego import GenericSet, Theme, Year

if t.TYPE_CHECKING:
    from sqlalchemy.orm import scoped_session

    from app.interfaces.daos.theme import IThemeDao
    from app.interfaces.daos.year import IYearDao


class SearchService:
    def __init__(
        self,
        *,
        db_session: "scoped_session",
        theme_dao: "IThemeDao",
        year_dao: "IYearDao"
    ) -> None:
        self.session = db_session
        self.theme_dao = theme_dao
        self.year_dao = year_dao

    def parse_query(self, query: str):
        keyword_regex = r'(\w+):(("(.*?)")|(\w+))'
        groups = re.findall(keyword_regex, query)
        keywords = [(group[0], group[3] or group[4]) for group in groups]
        return keywords, re.sub(
            r" +", " ", re.sub(keyword_regex, "", query).strip()
        )

    def search(
        self, search: str, keywords: dict, current_page: int, page_size: int
    ):
        select = (
            sa.select(GenericSet)
            .filter(GenericSet.is_minifig.is_(False))
            .join(Year, GenericSet.year_id == Year.id)
            .order_by(Year.name)
        )
        if len(search) > 0:
            select = select.filter(
                sa.or_(
                    GenericSet.id.contains(search),
                    GenericSet.name.contains(search),
                )
            )

        for key, value in keywords:
            if key == "theme":
                theme_ids = (
                    self.session.execute(
                        sa.select(Theme.id).filter(
                            Theme.name.contains(str(value))
                        )
                    )
                    .scalars()
                    .all()
                )
                if len(theme_ids) > 0:
                    select = select.filter(GenericSet.theme_id.in_(theme_ids))
            elif key == "year" and str(value).isnumeric():
                year_ids = (
                    self.session.execute(
                        sa.select(Year.id).filter(Year.name == int(value))
                    )
                    .scalars()
                    .all()
                )
                if len(year_ids) > 0:
                    select = select.filter(GenericSet.year_id.in_(year_ids))
            elif key == "name":
                select = select.filter(GenericSet.name.contains(str(value)))
            elif key == "id":
                select = select.filter(GenericSet.id.contains(str(value)))

        return db.paginate(select, page=current_page, per_page=page_size)

    def get_years(self):
        return [year.name for year in self.year_dao.all()]

    def get_themes(self):
        return [theme.name for theme in self.theme_dao.all()]
