# sqlib

### 安装prefect

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


#### 部署prefect

Deployment configuration saved to prefect.yaml! You can now deploy using this deployment configuration with:

部署配置已保存到 prefect.yaml！您现在可以使用此部署配置进行部署：

        $ prefect deploy -n default

You can also make changes to this deployment configuration by making changes to the prefect.yaml file.

您还可以通过更改 prefect.yaml 文件来更改此部署配置。

To execute flow runs from this deployment, start a worker in a separate terminal that pulls work from the 'default' work pool:

要从此部署执行流程运行，请在单独的终端中启动一个工作程序，从“默认”工作池中提取工作：

        $ prefect worker start --pool 'default'

To schedule a run for this deployment, use the following command:

要安排此部署的运行，请使用以下命令：

        $ prefect deployment run 'qlib_workflow/default'



#### 安装superset容器, 并设置登录用户名密码等
```
docker run -d -p 8080:8088 -v /home/idea/qlib/qlib_t/sqlib:/home/superset/app -e "SUPERSET_SECRET_KEY=sqlib1234" --name superset amancevice/superset

docker exec -it superset superset-init 
```

#### 进入superset容器, 并安装duckdb-engine
```
docker exec -it superset bash

pip install duckdb-engine -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 重启superset容器
```
docker restart superset
```

##沟通qq群:851540137
