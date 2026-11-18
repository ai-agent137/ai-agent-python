import unittest

from app.langgraph_persistence.graph_factory import add_user_message_to_state
from app.langgraph_persistence.service import LangGraphPersistenceService


class PersistenceServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = LangGraphPersistenceService()
        self.ids = dict(tenant_id="tenant_test", user_id="user_test", conversation_id="refund_test")

    def test_first_message_initializes_state(self):
        result = self.service.continue_flow(user_question="我要退款。", **self.ids)
        self.assertIsNone(result["order_status"])
        self.assertIsNone(result["order_id"])
        self.assertTrue(result["need_user_input"])
        self.assertEqual(result["waiting_for"], "order_id")
        self.assertEqual(len(result["messages"]), 2)

    def test_followup_preserves_history_and_refund_intent(self):
        self.service.continue_flow(user_question="我要退款。", **self.ids)
        result = self.service.continue_flow(user_question="订单号是 10002。", **self.ids)
        self.assertEqual(result["intent"], "refund")
        self.assertEqual(result["order_status"], "已付款，待发货")
        self.assertFalse(result["need_user_input"])
        self.assertIsNone(result["waiting_for"])
        self.assertEqual(len(result["messages"]), 4)
        self.assertEqual(len(result["logs"]), 8)

    def test_existing_partial_checkpoint_is_completed(self):
        config = self.service.build_config(self.service.build_thread_id(**self.ids))
        old_result = self.service.graph.invoke(add_user_message_to_state("我要退款。"), config=config)
        self.assertNotIn("order_status", old_result)
        result = self.service.continue_flow(user_question="我要退款。", **self.ids)
        self.assertIsNone(result["order_status"])
        self.assertEqual(len(result["messages"]), 4)
