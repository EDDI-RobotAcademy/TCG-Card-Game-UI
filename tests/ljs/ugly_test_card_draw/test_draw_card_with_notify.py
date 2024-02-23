import multiprocessing
import unittest

from notify_reader.controller.notify_reader_controller_impl import NotifyReaderControllerImpl
from task_worker.service.task_worker_service_impl import TaskWorkerServiceImpl


class TestDrawCardWithNotify(unittest.TestCase):
    def setUp(self):
        self.noWaitIpcChannel = multiprocessing.Queue()
        notifyReaderController = NotifyReaderControllerImpl.getInstance()
        notifyReaderController.requestToMappingNoticeWithFunction()
        notifyReaderController.requestToInjectNoWaitIpcChannel(self.noWaitIpcChannel)

        taskWorkerService = TaskWorkerServiceImpl.getInstance()
        taskWorkerService.createTaskWorker("NotifyReader", notifyReaderController.requestToReadNotifyCommand)
        taskWorkerService.executeTaskWorker("NotifyReader")

    def testNotifyReader(self):
        import tkinter
        root = tkinter.Tk()
        root.title("NotifyReader")

        btn = tkinter.Button(root, text="NOTICE!!")
        btn.place(relx=0.5, rely=0.5, anchor="center")

        def injectData(event):
            self.noWaitIpcChannel.put(
                '{"NOTIFY_DRAWN_CARD_LIST":{"player_drawn_card_list_map":{"You":[26,25,32]}}}')

        btn.bind("<Button-1>", injectData)

        root.mainloop()

if __name__ == '__main__':
    unittest.main()