import unittest

from app_window.service.window_service_impl import WindowServiceImpl
from task_worker.service.task_worker_service_impl import TaskWorkerServiceImpl


class TestDomainInitializer(unittest.TestCase):
    def test_initMainWindowDomain(self):
        # MainWindowServiceImpl이 정상적으로 생성되는지 확인
        window_service = WindowServiceImpl.getInstance()
        self.assertIsInstance(window_service, WindowServiceImpl)

    def test_initTaskWorkerDomain(self):
        # TaskWorkerServiceImpl이 정상적으로 생성되는지 확인
        task_worker_service = TaskWorkerServiceImpl.getInstance()
        self.assertIsInstance(task_worker_service, TaskWorkerServiceImpl)


if __name__ == '__main__':
    unittest.main()
    