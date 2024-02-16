import unittest
from unittest.mock import patch

from task_worker.service.task_worker_service_impl import TaskWorkerServiceImpl
from task_worker.repository.task_worker_repository_impl import TaskWorkerRepositoryImpl


class TestTaskWorkerServiceImpl(unittest.TestCase):
    def setUp(self):
        self.service = TaskWorkerServiceImpl()

    def test_singleton_instance(self):
        second_instance = TaskWorkerServiceImpl.getInstance()
        self.assertEqual(self.service, second_instance)

    def test_createTaskWorker(self):
        name = "TestWorker"
        will_be_execute_function = lambda x: x * 2

        with patch.object(TaskWorkerRepositoryImpl, 'saveTaskWorker') as mock_save:
            self.service.createTaskWorker(name, will_be_execute_function)

            mock_save.assert_called_once_with(name, will_be_execute_function)

    @patch("task_worker.repository.task_worker_repository_impl.TaskWorkerRepositoryImpl.executeTask")
    def test_executeTaskWorker(self, mock_execute_task):
        name = "TestWorker"
        will_be_execute_function = lambda _: print("hi")

        self.service.createTaskWorker(name, will_be_execute_function)
        self.service.executeTaskWorker(name)

        mock_execute_task.assert_called_once_with(name)


if __name__ == '__main__':
    unittest.main()
