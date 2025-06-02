from core.test_base.test_admin import TestAdminBase


class TranslationAdminTestCase(TestAdminBase):
    """Testing best developments image admin"""

    def setUp(self):
        super().setUp()
        self.endpoint = "/admin/translations/translationgroup/"

    def test_search_bar(self):
        """Validate search bar working"""

        self.submit_search_bar(self.endpoint)
