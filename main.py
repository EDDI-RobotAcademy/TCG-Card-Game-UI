from initializer.init_domain import DomainInitializer
from task_worker.service.task_worker_service_impl import TaskWorkerServiceImpl
from ui_frame.controller.ui_frame_controller_impl import UiFrameControllerImpl


DomainInitializer.initEachDomain()


if __name__ == "__main__":
    uiFrameController = UiFrameControllerImpl.getInstance()
    uiFrameController.requestToCreateUiFrame()

    # uiFrameController.requestToStartPrintGameUi()

    # rootWindow.mainloop()
    # uiFrameController.requestToStartPrintGameUi()

    taskWorkerService = TaskWorkerServiceImpl.getInstance()
    taskWorkerService.createTaskWorker("UI", uiFrameController.requestToStartPrintGameUi)
    taskWorkerService.executeTaskWorker("UI")
