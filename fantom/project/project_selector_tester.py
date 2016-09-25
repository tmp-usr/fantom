from storm.locals import *
from project_selector import ProjectSelector

fantomii_db= "../project/fantomii.db"

fantom_sqlite_db = create_database("sqlite:%s" % fantomii_db )
store= Store(fantom_sqlite_db)

ps= ProjectSelector("a", store)






