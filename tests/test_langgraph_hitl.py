import unittest

from app.core.exceptions import AppException
from app.langgraph_hitl.service import LangGraphHITLService


class HITLResumeTest(unittest.TestCase):
    def setUp(self):
        self.service = LangGraphHITLService()
        self.ids = dict(tenant_id="test", user_id="u_test", conversation_id="refund_test")

    def test_resume_without_start(self):
        with self.assertRaises(AppException) as raised:
            self.service.resume(**self.ids, decision={"type": "approve"})
        self.assertEqual(raised.exception.status_code, 404)
        self.assertFalse(self.service.get_state(**self.ids)["values"])

    def test_approve_and_prevent_duplicate_resume(self):
        self.service.start(**self.ids, user_question="我要退款，订单号10003")
        result = self.service.resume(**self.ids, decision={"type": "approve"})["result"]
        self.assertTrue(result["action_result"]["success"])
        self.assertEqual(result["user_question"], "我要退款，订单号10003")
        with self.assertRaises(AppException) as raised:
            self.service.resume(**self.ids, decision={"type": "approve"})
        self.assertEqual(raised.exception.status_code, 409)

    def test_reject(self):
        self.service.start(**self.ids, user_question="我要退款，订单号10003")
        result = self.service.resume(**self.ids, decision={"type": "reject", "reason": "不符合规则"})["result"]
        self.assertFalse(result["action_result"]["success"])
        self.assertEqual(result["action_result"]["reason"], "不符合规则")

    def test_completed_flow_does_not_accept_resume(self):
        self.service.start(**self.ids, user_question="你好")
        with self.assertRaises(AppException) as raised:
            self.service.resume(**self.ids, decision={"type": "approve"})
        self.assertEqual(raised.exception.status_code, 409)
