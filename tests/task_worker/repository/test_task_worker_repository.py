import unittest
from multiprocessing import Process
from unittest.mock import patch, Mock

from task_worker.entity.task_worker import TaskWorker
from task_worker.repository.task_worker_repository_impl import TaskWorkerRepositoryImpl


class TestTaskControlRepositoryImpl(unittest.TestCase):
    def setUp(self):
        self.repository = TaskWorkerRepositoryImpl()

    def test_singleton_instance(self):
        second_instance = TaskWorkerRepositoryImpl.getInstance()
        self.assertEqual(self.repository, second_instance)

    def test_save_task_worker(self):
        name = "TestWorker"
        will_be_execute_function = lambda x: x * 2

        self.assertEqual(len(self.repository._TaskWorkerRepositoryImpl__thread_worker_list), 0)

        self.repository.saveTaskWorker(name, will_be_execute_function)
        self.assertEqual(len(self.repository._TaskWorkerRepositoryImpl__thread_worker_list), 1)

        saved_task_worker = self.repository._TaskWorkerRepositoryImpl__thread_worker_list.get(name)
        self.assertIsInstance(saved_task_worker, TaskWorker)
        self.assertEqual(saved_task_worker.getName(), name)
        self.assertEqual(saved_task_worker.getWillBeExecuteFunction(), will_be_execute_function)

    def test_execute_task(self):

        name = "TestWorker"
        will_be_execute_function = lambda _: print("\nhello")
        will_be_execute_function(None)

        self.repository.saveTaskWorker(name, will_be_execute_function)
        self.repository.executeTask(name)

        task_worker_before = self.repository._TaskWorkerRepositoryImpl__thread_worker_list[name]
        print("TaskWorker before execution:", task_worker_before)
        self.assertIsNone(task_worker_before.getTaskPid())

        with patch("multiprocessing.Process", autospec=True) as mock_process:
            mock_process_instance = Mock(spec=Process)
            mock_process.return_value = mock_process_instance

            self.repository.executeTask(name)

            task_worker_after = self.repository._TaskWorkerRepositoryImpl__thread_worker_list[name]
            print("TaskWorker after execution:", task_worker_after)
            self.assertEqual(task_worker_after.getTaskPid(), mock_process_instance.pid)


if __name__ == '__main__':
    unittest.main()
