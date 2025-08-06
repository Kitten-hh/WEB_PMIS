#!/bin/bash

# 检查是否传入版本参数
if [ -z "$1" ]; then
  echo "Usage: $0 <Release>"
  exit 1
fi

RELEASE_VERSION=$1

# 获取当前脚本文件的所在目录
SCRIPT_DIR=$(dirname "$(realpath "$0")")
echo "Script directory: $SCRIPT_DIR"


# 查找 manage.py 文件並從中獲取項目名稱
MANAGE_PY_PATH=$(find "$SCRIPT_DIR" -name "manage.py" -print -quit)

# 檢查manage.py 是否存在
if [ -z "$MANAGE_PY_PATH" ]; then
    echo "Error: manage.py not found in or above"
    exit 1
fi


# 從manage.py 文件中提取 DJANGO_SETTINGS_MODULE 環境變量的值中取得項目的名稱
PROJECT_NAME=$(grep -Po "(?<=os.environ.setdefault\(['\"]DJANGO_SETTINGS_MODULE['\"], ['\"])\w+" "$MANAGE_PY_PATH")
if [ -z "$PROJECT_NAME" ]; then
  echo "Error: Could not extract project name from manage.py."
  exit 1
fi

echo "Project Name: $PROJECT_NAME"

# 啟動前端服務並放到後臺運行
echo "Starting npm run serve..."
npm run serve 2>&1 > npm_run_serve.log &  # 將 npm 的輸出重定向到檔並放入後臺
NPM_PID=$!  # 直接獲取 npm 的 PID

# 將日誌檔內容發送到 tee，繼續輸出到終端
tee -a npm_run_serve.log <&0 &

echo "npm run serve is running in the background with PID $NPM_PID. Waiting for server to be ready..."

# 迴圈檢查日誌檔，直到發現"Executing additional scripts before exit"或遇到錯誤
while true; do
  if grep -i "error" npm_run_serve.log; then
    echo "Error: npm run serve encountered errors."
    kill $NPM_PID
    exit 1
  fi

  if grep -q "Executing additional scripts before exit" npm_run_serve.log; then
    echo "npm run serve completed successfully."
    break
  fi

  echo "Waiting for the server to finish compiling..."
  sleep 5  # 等待 5 秒後再次檢查
done

# 收集靜態檔
SETTINGS_MODULE="${PROJECT_NAME}.settings_${RELEASE_VERSION}"
echo "Collecting static files using settings: $SETTINGS_MODULE"
python3 manage.py collectstatic --settings="$SETTINGS_MODULE" --noinput --pythonpath="$SCRIPT_DIR"
if [ $? -ne 0 ]; then
  echo "Error: collectstatic failed."
  kill $NPM_PID
  exit 1
fi

# 查找並殺死正在使用的進程
echo "Stopping existing uwsgi process..."
while true; do
  UWSGI_PID=$(ps -ef | grep "${PROJECT_NAME}_${RELEASE_VERSION}.xml" | grep -v grep | awk '{print $2}')

  if [ -n "$UWSGI_PID" ]; then
    echo "Killing process ID(s): $UWSGI_PID"
    kill -9 $UWSGI_PID
    sleep 1  # 等待一秒後再次檢查
  else
    echo "All related uwsgi processes have been stopped."
    break
  fi
done

# 啟動新的 uwsgi 服務
echo "Starting uwsgi with configuration ${PROJECT_NAME}_${RELEASE_VERSION}.xml..."
uwsgi -x "${PROJECT_NAME}_${RELEASE_VERSION}.xml"
if [ $? -ne 0 ]; then
  echo "Error: uwsgi start failed."
  kill $NPM_PID
  exit 1
fi

# 確保在所有操作完成後殺掉 npm run serve 進程及其子進程
if [ -n "$NPM_PID" ]; then
  echo "Killing npm run serve process with PID $NPM_PID"
  pkill -P $NPM_PID
fi
echo "Deployment completed."
