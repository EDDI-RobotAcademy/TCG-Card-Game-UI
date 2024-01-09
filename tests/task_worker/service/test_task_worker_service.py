import unittest
from unittest.mock import patch

from task_worker.service.task_worker_service_impl import TaskWorkerServiceImpl
from task_worker.repository.task_worker_repository_impl import TaskWorkerRepositoryImpl


class TestTaskWorkerServiceImpl(unittest.TestCase):
    def setUp(self):
        # 테스트용 TaskWorkerServiceImpl 인스턴스 생성
        self.service = TaskWorkerServiceImpl()

    def test_singleton_instance(self):
        # 두 번째 인스턴스가 첫 번째 인스턴스와 동일한지 확인
        second_instance = TaskWorkerServiceImpl.getInstance()
        self.assertEqual(self.service, second_instance)

    def test_createTaskWorker(self):
        # createTaskWorker 메서드가 정상적으로 동작하는지 확인
        name = "TestWorker"
        will_be_execute_function = lambda x: x * 2

        # Mock을 이용하여 repository의 save_task_worker 메서드의 동작을 확인
        with patch.object(TaskWorkerRepositoryImpl, 'save_task_worker') as mock_save:
            self.service.createTaskWorker(name, will_be_execute_function)

            # save_task_worker 메서드가 호출되었는지 확인
            mock_save.assert_called_once_with(name, will_be_execute_function)


if __name__ == '__main__':
    unittest.main()
