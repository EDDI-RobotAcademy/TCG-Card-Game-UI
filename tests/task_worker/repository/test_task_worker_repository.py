import unittest
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

        self.repository.save_task_worker(name, will_be_execute_function)
        self.assertEqual(len(self.repository._TaskWorkerRepositoryImpl__thread_worker_list), 1)

        saved_task_worker = self.repository._TaskWorkerRepositoryImpl__thread_worker_list.get(name)
        self.assertIsInstance(saved_task_worker, TaskWorker)
        self.assertEqual(saved_task_worker.getName(), name)
        self.assertEqual(saved_task_worker.getWillBeExecuteFunction(), will_be_execute_function)

if __name__ == '__main__':
    unittest.main()
