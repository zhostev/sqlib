# 创建项目根目录
mkdir quant-trading-backend

# 进入项目根目录
cd quant-trading-backend

# 创建应用目录和子目录
mkdir -p app/routes app/services app/utils

# 创建测试目录和测试文件
mkdir tests
touch tests/__init__.py
touch tests/test_config.py
touch tests/test_data.py
touch tests/test_evaluation.py
touch tests/test_model.py

# 创建应用的 __init__.py 文件
touch app/__init__.py

# 创建路由文件
touch app/routes/__init__.py
touch app/routes/config_routes.py
touch app/routes/data_routes.py
touch app/routes/evaluation_routes.py
touch app/routes/model_routes.py

# 创建服务文件
touch app/services/__init__.py
touch app/services/config_service.py
touch app/services/data_service.py
touch app/services/evaluation_service.py
touch app/services/model_service.py

# 创建工具文件
touch app/utils/__init__.py
touch app/utils/db_utils.py

# 创建 requirements.txt 文件用于指定依赖
touch requirements.txt

# 创建环境变量文件
touch .env
touch .flaskenv

# 创建 Flask 配置文件
touch config.py

# 创建 Flask 启动文件
touch run.py

# 输出目录结构
tree