from utils.automation import get_selenium_elems

from core.test_base.test_admin import TestAdminBase


class PropertyAdminTestCase(TestAdminBase):
    
    def setUp(self):
        
        # Submit endpoint
        super().setUp("/admin/properties/property/add")

    def test_markdown_editor_loaded(self):
        """
        Check if the editor is loaded with reference elements
        """
        
        selectors = {
            "tool_bar": '.editor-toolbar',
            "bold": 'a[title="Bold (Ctrl-B)"]',
            "editor": '.CodeMirror-scroll',
            "status_bar": '.editor-statusbar'
        }
        elems = get_selenium_elems(self.driver, selectors)
        for elem_name, elem in elems.items():
            self.assertTrue(elem, f"Element {elem_name} not found")