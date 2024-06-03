from starlette.config import Config
from sqlalchemy import create_engine, MetaData
from sqlalchemy.pool import NullPool
import databases
config = Config(".env")

DB_HOST = config("DB_HOST", default="")
DB_PORT = config("DB_PORT", default="")
DB_DATABASE = config("DB_DATABASE", default="")
DB_USERNAME = config("DB_USERNAME", default="")
DB_PASSWORD = config("DB_PASSWORD", default="")
DB_URL = "postgresql://{}:{}@{}:{}/{}".format(
    DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE
)
print("DB_URL: ", DB_URL)
CONNECTION = databases.Database(DB_URL)
# Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# engine = create_engine(
#     DB_URL
# )
# META_DATA = MetaData()
# META_DATA.reflect(bind=engine)
# db_session = scoped_session(
#     sessionmaker(
#         autocommit=False, 
#         autoflush=False, 
#         bind=engine,
#         expire_on_commit=False
#     )
# )