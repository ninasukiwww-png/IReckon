#!/usr/bin/env python3
import asyncio, io, os, signal, sys
os.environ["UVICORN_ACCESS_LOGGING"] = "0"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
from app.core.logger import setup_logging, logger
from app.core.database import db
from app.core.config import config_manager
from app.core.updater import updater
from app.llm.client import capability_pool
from app.engine.tasks import task_manager
from app.engine.learner import idle_loop
from app.web.ws import log_consumer
from app.tools.registry import register_builtin_tools

class IReckonApp:
    def __init__(self):
        self._shutdown_event = asyncio.Event()
        self._tasks = []

    async def initialize(self):
        setup_logging()
        logger.info(f"启动 {config_manager.get('system.name')} v{config_manager.get('system.version')}")
        await self._check_update()
        await db.connect()
        await capability_pool.refresh()
        await register_builtin_tools()
        self._tasks.append(asyncio.create_task(idle_loop.run()))
        self._tasks.append(asyncio.create_task(log_consumer()))
        logger.info("系统初始化完成")

    async def _check_update(self):
        if not updater.should_check():
            return
        updater.mark_checked()
        version = await updater.check()
        if version:
            logger.info(f"发现新版本 v{version}，请运行 python scripts/update.py 进行更新")

    async def shutdown(self):
        logger.info("正在关闭系统...")
        self._shutdown_event.set()
        for task in self._tasks:
            task.cancel()
            try: await task
            except asyncio.CancelledError: pass
        await db.close()
        logger.info("系统已关闭")

async def start_backend():
    import uvicorn
    import logging
    logging.getLogger("uvicorn.access").handlers = []
    logging.getLogger("uvicorn.access").propagate = False
    host = config_manager.get("server.host", "0.0.0.0")
    port = config_manager.get("server.port", 8000)
    log_level = config_manager.get("server.log_level", "info")
    config = uvicorn.Config("app.web.api:app", host=host, port=port, log_level=log_level, loop="asyncio", access_log=False)
    logger.info(f"\n{'='*50}\n  IReckon 服务已启动\n{'='*50}\n"
                f"  API:       http://{host}:{port}\n"
                f"  文档:      http://{host}:{port}/docs\n"
                f"  前端:      http://localhost:8501\n"
                f"  状态检查:  http://{host}:{port}/api/health\n"
                f"{'='*50}")
    await uvicorn.Server(config).serve()

async def main():
    app = IReckonApp()
    await app.initialize()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try: loop.add_signal_handler(sig, lambda: asyncio.create_task(app.shutdown()))
        except NotImplementedError: pass
    backend_task = asyncio.create_task(start_backend())
    try: await app._shutdown_event.wait()
    finally:
        backend_task.cancel() 
        try: await backend_task
        except asyncio.CancelledError: pass
        await app.shutdown()

if __name__ == "__main__":
    asyncio.run(main())