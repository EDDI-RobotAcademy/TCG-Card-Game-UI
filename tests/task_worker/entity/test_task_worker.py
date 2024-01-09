import unittest
from task_worker.entity.task_worker import TaskWorker

class TestTaskWorker(unittest.TestCase):
    def setUp(self):
        # 테스트용 TaskWorker 인스턴스 생성
        self.task_worker = TaskWorker("TestWorker", lambda x: x * 2)

    def test_getName(self):
        # getName 메서드가 올바른 이름을 반환하는지 테스트
        self.assertEqual(self.task_worker.getName(), "TestWorker")

    def test_getWillBeExecuteFunction(self):
        # getWillBeExecuteFunction 메서드가 올바른 함수를 반환하는지 테스트
        expected_function = lambda x: x * 2
        actual_function = self.task_worker.getWillBeExecuteFunction()

        print(f"expected_function: {expected_function(5)}")
        print(f"actual_function: {actual_function(5)}")

        # 함수의 바이트코드
        self.assertEqual(actual_function.__code__.co_code, expected_function.__code__.co_code)
        # 함수의 지역 변수 이름
        self.assertEqual(actual_function.__code__.co_varnames, expected_function.__code__.co_varnames)

if __name__ == '__main__':
    unittest.main()
