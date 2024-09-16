#!/bin/bash

# 控制脚本的名称
SCRIPT_NAME="main.py"
PID_FILE="main.pid"

# 启动脚本
start() {
    if [ -f "$PID_FILE" ]; then
        echo "Script is already running (PID: $(cat $PID_FILE))."
        exit 1
    fi
    
    echo "Starting script..."
    nohup python "$SCRIPT_NAME" > /dev/null 2>&1 &
    echo $! > "$PID_FILE"
    echo "Script started (PID: $(cat $PID_FILE))."
}

# 停止脚本
stop() {
    if [ ! -f "$PID_FILE" ]; then
        echo "Script is not running."
        exit 1
    fi
    
    PID=$(cat "$PID_FILE")
    echo "Stopping script (PID: $PID)..."
    kill -9 "$PID"
    rm -f "$PID_FILE"
    echo "Script stopped."
}

# 重启脚本
restart() {
    stop
    sleep 2
    start
}

# 确保传递了参数
if [ $# -eq 0 ]; then
    echo "Usage: $0 {start|stop|restart}"
    exit 1
fi

# 根据参数执行相应的操作
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac
