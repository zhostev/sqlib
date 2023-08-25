#!/bin/bash

# 添加所有修改的文件到暂存区
git add --all :!*.db

# 提交修改
read -p "请输入提交说明: " message
git commit -m "$message"

# 推送到远程仓库
git push origin main
