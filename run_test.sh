#!/bin/bash

msg=" Running pytest with coverage report start "
cols=$(tput cols)

# 算出左右箭頭長度
padding=$(( (cols - ${#msg}) / 2 ))
left=$(printf '%*s' "$padding" '' | tr '    ' '>')
right=$(printf '%*s' "$padding" '' | tr '    ' '<')

# 左右箭頭黃色，msg 粗體
echo -e "\033[33m${left}\033[0m\033[1m${msg}\033[0m\033[33m${right}\033[0m"

pytest --cov=apps --cov-report=term-missing