

# sqlib
![1693787547221245883C80F181C4A](https://github.com/zhostev/sqlib/assets/57177476/edbec924-f19c-4855-9263-0d901aeaa0ac)

ProjectName and Description

![sqlib方案](https://github.com/vinsvison/sqlib/assets/57177476/d13aeb33-b400-469b-9faf-604036c0a21e)

<p align="center">
  <h3 align="center">"sqlib介绍</h3>
  <p align="center">
    一个"完美的"README去快速开始你的项目！
    <br />
    <a href="https://github.com/vinsvison/sqlib"><strong>探索本项目的文档 »</strong></a>
    <br />
    <br />
    <a href="https://github.com/vinsvison/sqlib">查看Demo</a>
    ·
    <a href="https://github.com/vinsvison/sqlib">报告Bug</a>
    ·
    <a href="https://github.com/vinsvison/sqlib">提出新特性</a>
  </p>

</p>


 本篇README.md面向开发者

## 目录

- [上手指南](#上手指南)
  - [开发前的配置要求](#开发前的配置要求)
  - [安装步骤](#安装步骤)
- [文件目录说明](#文件目录说明)
- [开发的架构](#开发的架构)
- [部署](#部署)
- [使用到的框架](#使用到的框架)
- [贡献者](#贡献者)
  - [如何参与开源项目](#如何参与开源项目)
- [版本控制](#版本控制)
- [作者](#作者)
- [鸣谢](#鸣谢)

### 上手指南

请将所有链接中的“shaojintian/Best_README_template”改为“your_github_name/your_repository”



###### 开发前的配置要求

1. 本版本支持Ubuntu，其他系统未作详细测试。
2. 依赖微软量化交易平台qlib。

###### **安装步骤**

1. 安装qlib
2. Clone the repo

```sh
git clone https://github.com/vinsvison/sqlib.git
```

### 文件目录说明
```
filetree 
├── ARCHITECTURE.md
├── LICENSE.txt
├── README.md
├── /account/
├── /bbs/
├── /docs/
│  ├── /rules/
│  │  ├── backend.txt
│  │  └── frontend.txt
├── manage.py
├── /oa/
├── /static/
├── /templates/
├── useless.md
└── /util/

```

### 开发的架构 

请阅读[ARCHITECTURE.md]() 查阅为该项目的架构。

### 部署


#### 1、qlib安装

具体参考：https://qlib.readthedocs.io/en/latest/start/installation.html
可以直接 pip install qlib
若需要修改源码的，建议源码安装。

```
pip install numpy
pip install --upgrade cython
git clone https://github.com/microsoft/qlib.git && cd qlib
python setup.py install
```

特别说明：支持python==3.8版本。

#### 2、安装mlflow

具体参考：https://github.com/Toumash/mlflow-docker

根据自己的实际情况修改`.env`

执行几个sh脚本后，运行`docker-compose up -d`

特别说明：也可以直接 pip install mlflow
然后mlflow ui 启动服务
<img width="1078" alt="image" src="https://github.com/vinsvison/sqlib/assets/57177476/3cb6217a-ffa1-4222-9e39-345ddec831e1">

#### 3、安装prefect

#### 启动postgres

```
docker run -d --name prefect-postgres -v prefectdb:/var/lib/postgresql/data -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=prefect -e POSTGRES_DB=prefect postgres:latest
```

##### 安装prefect包

```
pip install prefect
```

##### 设置prefect数据库

```
prefect config set PREFECT_API_DATABASE_CONNECTION_URL="postgresql+asyncpg://postgres:prefect@localhost:5432/prefect"
```

##### 启动

```
docker start prefect-postgres
prefect server start
```
<img width="1079" alt="image" src="https://github.com/vinsvison/sqlib/assets/57177476/4a5e7f40-c1eb-4786-b5d5-6bd1e57879de">


#### 4、安装superset容器, 并设置登录用户名密码等

```
docker run -d -p 8080:8088 -v /home/idea/qlib/qlib_t/sqlib:/home/superset/app -e "SUPERSET_SECRET_KEY=sqlib1234" --name superset amancevice/superset

docker exec -it superset superset-init 
```

##### 进入superset容器, 并安装duckdb-engine

```
docker exec -it superset bash

pip install duckdb-engine -i https://pypi.tuna.tsinghua.edu.cn/simple

exit
```

##### 重启superset容器

```
docker restart superset
```

### 使用到的框架

- qlib
- mlflow
- prefect
- superset
- duckdb


![sqlib股票回测评估系统-2023-09-04T06-03-43 690Z](https://github.com/zhostev/sqlib/assets/57177476/50f23a65-011b-424c-ae89-6abb692db666)

### 贡献者

请阅读**CONTRIBUTING.md** 查阅为该项目做出贡献的开发者。

#### 如何参与开源项目

贡献使开源社区成为一个学习、激励和创造的绝佳场所。你所作的任何贡献都是**非常感谢**的。


1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 版本控制

该项目使用Git进行版本管理。您可以在repository参看当前可用版本。

### 作者

ujujzhao@gmail.com

知乎:zhihu.com/people/ideaplat&ensp; qq group : 851540137

 *您也可以在贡献者名单中参看所有参与该项目的开发者。*

### 版权说明

该项目签署了MIT 授权许可，详情请参阅 [LICENSE.txt](https://github.com/shaojintian/Best_README_template/blob/master/LICENSE.txt)

### 鸣谢


<!-- links -->



