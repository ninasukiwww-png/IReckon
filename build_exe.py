import os
import shutil
import subprocess
import sys
from pathlib import Path

DIST = Path("dist") / "IReckon"
BUILD = Path("build")


def clean():
    for d in [DIST, BUILD]:
        if d.exists():
            shutil.rmtree(d)


def build_backend():
    print("=== 构建后端 ===")
    subprocess.check_call([
        sys.executable, "-m", "PyInstaller",
        "--name", "ireckon-backend",
        "--distpath", str(DIST),
        "--workpath", str(BUILD),
        "--add-data", f"config{os.pathsep}config",
        "--hidden-import", "app.web.api",
        "--hidden-import", "app.engine.self_improve",
        "--hidden-import", "app.engine.style",
        "--hidden-import", "app.engine.learner",
        "--hidden-import", "app.engine.registry",
        "--hidden-import", "app.engine.tasks",
        "--hidden-import", "app.engine.room",
        "--hidden-import", "app.engine.machine",
        "--hidden-import", "app.engine.board",
        "--hidden-import", "app.engine.detector",
        "--hidden-import", "app.engine.cost",
        "--hidden-import", "app.agents.base",
        "--hidden-import", "app.agents.executor",
        "--hidden-import", "app.agents.scheduler",
        "--hidden-import", "app.agents.reviewer",
        "--hidden-import", "app.agents.creative",
        "--hidden-import", "app.agents.deliverer",
        "--hidden-import", "app.agents.learner",
        "--hidden-import", "app.agents.tool_manager",
        "--hidden-import", "app.agents.content_filter",
        "--hidden-import", "app.llm.client",
        "--hidden-import", "app.llm.pool",
        "--hidden-import", "app.tools.registry",
        "--hidden-import", "app.tools.library",
        "--hidden-import", "app.tools.assembler",
        "--hidden-import", "app.security.scanner",
        "--hidden-import", "app.security.filter",
        "--hidden-import", "app.security.sandbox",
        "--hidden-import", "app.security.mining",
        "--hidden-import", "app.security.supply",
        "--hidden-import", "app.knowledge.vector",
        "--hidden-import", "app.knowledge.files",
        "--hidden-import", "app.web.ws",
        "--hidden-import", "app.web.push",
        "--hidden-import", "app.core.updater",
        "--hidden-import", "uvicorn",
        "--hidden-import", "multipart",
        "--hidden-import", "watchdog",
        "--collect-submodules", "chromadb",
        "--noconfirm",
        "--onedir",
        "main.py",
    ])
    print("后端构建完成")


def build_frontend():
    print("=== 构建前端 ===")
    subprocess.check_call([
        sys.executable, "-m", "PyInstaller",
        "--name", "ireckon-frontend",
        "--distpath", str(DIST),
        "--workpath", str(BUILD),
        "--add-data", f"ui{os.pathsep}ui",
        "--add-data", f"config{os.pathsep}config",
        "--add-data", f".streamlit{os.pathsep}.streamlit",
        "--hidden-import", "streamlit.web.bootstrap",
        "--collect-all", "streamlit",
        "--collect-all", "Pillow",
        "--noconfirm",
        "--onedir",
        "run_streamlit.py",
    ])
    print("前端构建完成")


def create_launcher():
    launcher = """@echo off
title IReckon AI Factory v2.1.0
echo ============================================
echo   IReckon AI Factory v2.1.0
echo ============================================
echo.
start "" "%~dp0ireckon-backend\ireckon-backend.exe"
echo [BACKEND] 启动中... (port 8000)
timeout /t 3 /nobreak >nul
start "" "%~dp0ireckon-frontend\ireckon-frontend.exe"
echo [FRONTEND] 启动中... (port 8501)
timeout /t 5 /nobreak >nul
echo.
echo   Backend: http://localhost:8000/docs
echo   Frontend: http://localhost:8501
echo.
start http://localhost:8501
echo 关闭此窗口即可停止服务
echo.
pause >nul
taskkill /f /im ireckon-backend.exe >nul 2>&1
taskkill /f /im ireckon-frontend.exe >nul 2>&1
"""
    (DIST / "启动IReckon.bat").write_text(launcher, encoding="gbk")
    print("启动脚本已创建")


def main():
    clean()
    build_backend()
    build_frontend()
    create_launcher()
    size = sum(f.stat().st_size for f in DIST.rglob("*") if f.is_file())
    print(f"\n✅ 打包完成! 输出: {DIST}")
    print(f"   总大小: {size / 1024 / 1024:.0f} MB")
    print(f"   运行 {DIST / '启动IReckon.bat'} 即可启动")


if __name__ == "__main__":
    main()