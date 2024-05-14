#!/bin/bash

# 设置目标目录
TARGET_DIR="/home/idea/code/sqlib_v2"

# 设置输出文件
OUTPUT_FILE="${TARGET_DIR}/all_codes_with_paths.txt"

# 清空现有的输出文件，如果它已经存在
> "$OUTPUT_FILE"

# 查找文件并追加它们的路径和内容到输出文件
find "$TARGET_DIR" -type f \( -name "*.py" -o -name "*.java" \) | while read file; do
    echo "File: $file" >> "$OUTPUT_FILE"
    cat "$file" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE" # 添加空行作为文件间的分隔
done

echo "All code files, along with their paths, have been written to $OUTPUT_FILE."
