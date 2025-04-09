from utils.automation import get_selenium_elems

from core.test_base.test_admin import TestAdminSeleniumBase


class PostAdminTestCase(TestAdminSeleniumBase):
    
    def setUp(self):
        
        # Submit endpoint
        super().setUp("/admin/blog/post/add")
        
        self.markdown_selectors = {
            "tool_bar": '.editor-toolbar',
            "bold": 'a[title="Bold (Ctrl-B)"]',
            "editor": '.CodeMirror-scroll',
            "status_bar": '.editor-statusbar'
        }

    def test_markdown_editor_loaded(self):
        """ Check if markdown is not allowed in google maps src """
        
        elems = get_selenium_elems(self.driver, self.markdown_selectors)
        for elem_name, elem in elems.items():
            self.assertTrue(elem, f"Element {elem_name} not found")
        
    def test_no_markdown_in_description(self):
        """
        Check if the editor is loaded with reference elements
        """
        
        # Add wrapper class to each markdown element
        wrapper_class = "field-description"
        for elem_name, elem in self.markdown_selectors.items():
            self.markdown_selectors[elem_name] = f".{wrapper_class} {elem}"
        
        elems = get_selenium_elems(self.driver, self.markdown_selectors)
        for elem_name, elem in elems.items():
            self.assertIsNone(elem, f"Element {elem_name} found (should not be found)")