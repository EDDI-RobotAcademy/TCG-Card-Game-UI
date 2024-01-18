import unittest

from initializer.init_domain import DomainInitializer
from task_worker.service.task_worker_service_impl import TaskWorkerServiceImpl
from ui_frame.controller.ui_frame_controller_impl import UiFrameControllerImpl


class TestTaskWorker(unittest.TestCase):
    def setUp(self):
        DomainInitializer.initEachDomain()

    def test_lobby_frame(self):
        uiFrameController = UiFrameControllerImpl.getInstance()
        uiFrameController.requestToCreateUiFrame()
        uiFrameController.switchFrameWithMenuName("lobby-menu")

        taskWorkerService = TaskWorkerServiceImpl.getInstance()
        taskWorkerService.createTaskWorker("UI", uiFrameController.requestToStartPrintGameUi)
        taskWorkerService.executeTaskWorker("UI")

        while True:
            pass


if __name__ == '__main__':
    unittest.main()

