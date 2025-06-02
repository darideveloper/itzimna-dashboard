from core.test_base.test_admin import TestAdminBase


class BestDevelopmentsImageAdminTestCase(TestAdminBase):
    """Testing best developments image admin"""

    def setUp(self):
        super().setUp()
        self.endpoint = "/admin/content/bestdevelopmentsimage/"

    def test_search_bar(self):
        """Validate search bar working"""

        self.submit_search_bar(self.endpoint)
