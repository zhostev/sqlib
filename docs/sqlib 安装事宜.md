# sqlib 安装事宜

## 1、qlib安装

具体参考：https://qlib.readthedocs.io/en/latest/start/installation.html

若需要修改源码的，建议源码安装。

```
pip install numpy
pip install --upgrade cython
git clone https://github.com/microsoft/qlib.git && cd qlib
python setup.py install
```

特别说明：支持python==3.8版本。

## 2、安装mlflow

具体参考：https://github.com/Toumash/mlflow-docker

根据自己的实际情况修改`.env`

执行几个sh脚本后，运行`docker-compose up -d`

## 3、安装prefect

#### 启动postgres

```
docker run -d --name prefect-postgres -v prefectdb:/var/lib/postgresql/data -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=prefect -e POSTGRES_DB=prefect postgres:latest
```
#### 安装prefect包
```
pip install prefect
```

#### 设置prefect数据库

```
prefect config set PREFECT_API_DATABASE_CONNECTION_URL="postgresql+asyncpg://postgres:prefect@localhost:5432/prefect"
```

#### 启动

```
docker start prefect-postgres
prefect server start
```

## 4、安装superset

#### 安装superset
```
docker run -d -p 8080:8088 -v /home/idea/qlib/qlib_t/sqlib:/home/superset/app -e "SUPERSET_SECRET_KEY=sqlib1234" --name superset amancevice/superset

docker exec -it superset superset-init 

pip install duckdb-engine -i https://pypi.tuna.tsinghua.edu.cn/simple
```

特别说明一下：`/home/idea/qlib/qlib_t/sqlib:/home/superset/app`

你保存到本地的地址为：`/home/idea/qlib/qlib_t/sqlib`，需要映射到容器的对应地址：`/home/superset/app`

#### 重启superset

```
docker restart superset
```