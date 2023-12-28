# 创建项目目录
mkdir quant-trading-platform

# 进入项目目录
cd quant-trading-platform

# 创建组件目录和子目录
mkdir -p components/ConfigEditor components/DataManagement components/ModelManagement components/Evaluation

# 创建页面目录
mkdir pages

# 创建公共资源目录
mkdir public

# 创建样式目录
mkdir styles

# 创建工具函数目录
mkdir utils

# 创建配置Schema目录
mkdir schemas

# 创建组件文件
touch components/ConfigEditor/ConfigEditor.js
touch components/ConfigEditor/ConfigForm.js
touch components/DataManagement/DataInitiator.js
touch components/DataManagement/DataStatus.js
touch components/ModelManagement/ModelTraining.js
touch components/ModelManagement/TrainingStatus.js
touch components/Evaluation/EvaluationResults.js
touch components/Evaluation/PerformanceCharts.js

# 创建页面文件
touch pages/index.js
touch pages/config.js
touch pages/data.js
touch pages/model.js
touch pages/evaluation.js

# 创建样式文件
touch styles/globals.css

# 创建工具函数文件
touch utils/api.js

# 创建配置Schema文件
touch schemas/config-schema.json

# 创建环境变量文件和配置文件
touch .env
touch next.config.js

# 创建 package.json 和 README.md
touch package.json
touch README.md

# 输出目录结构
tree