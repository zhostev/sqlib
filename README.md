# sqlib

### 安装prefect

#### 启动postgres

```
docker run -d --name prefect-postgres -v prefectdb:/var/lib/postgresql/data -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=prefect -e POSTGRES_DB=prefect postgres:latest
```

#### 设置prefect数据库

```
prefect config set PREFECT_API_DATABASE_CONNECTION_URL="postgresql+asyncpg://postgres:prefect@localhost:5432/prefect"
```

#### 启动

```
 prefect server start
```































##沟通qq群
![image](https://github.com/vinsvison/sqlib/assets/57177476/10f5c2f5-7929-424e-b94b-61ae1c711580)
