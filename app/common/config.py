#%%
from dataclasses import dataclass, asdict
from lib2to3.pytree import Base
from os import path, environ


## app폴더를 base 폴더로 지정함  파일 -> common -> app
base_dir= path.dirname(path.dirname(path.abspath(__file__)))

## dataclass 데코레이터 라이브러리를 사용하여 해당 클래스를 dic형태로 변환하여 사용
# ex) asdict(LocalConfig()), asdict(Config)
@dataclass
class Config:
    """
    기본 config
    """
    BASE_DIR= base_dir
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True

@dataclass
class LocalConfig(Config):
    PROJ_RELOAD: bool = True


@dataclass
class ProdConfig(Config):
    PROJ_RELOAD: bool = False


def conf():
    """
    환경 불러오기
    :return:
    """
    config = dict(prod=ProdConfig(), local=LocalConfig())
    return config.get(environ.get("API_ENV", "local"))




#%%
print(asdict(LocalConfig())['PROJ_RELOAD'])
