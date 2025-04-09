from time import sleep

from core.test_base.test_admin import TestAdminSeleniumBase
from blog import models
from utils.media import get_test_image


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
        
        elems = self.get_selenium_elems(self.markdown_selectors)
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
        
        elems = self.get_selenium_elems(self.markdown_selectors)
        for elem_name, elem in elems.items():
            self.assertIsNone(elem, f"Element {elem_name} found (should not be found)")
        
            
class ImageAdminTestCase(TestAdminSeleniumBase):
    
    def setUp(self):
        
        # Create image instance
        self.image = models.Image.objects.create(
            name="Test Image",
        )
        image_file = get_test_image()
        self.image.image = image_file
        self.image.save()
        self.image.refresh_from_db()
        
        # Login
        super().setUp()
        
        self.endpoint = "/admin/blog/image"
        
    def test_image_list_view(self):
        """ Check if image list view is loaded """
        
        # Submit endpoint
        self.set_page(self.endpoint)
        sleep(2)
        
        # Check if image is displayed in list view
        image_elem = self.get_selenium_elems(
            {
                "image": f"img[src*='{self.image.image.url}']",
            }
        )["image"]
        self.assertTrue(image_elem, "Image not found in list view")
        
    def test_image_detail_view(self):
        """ Check if image detail view is loaded """
        
        # Submit endpoint
        self.set_page(f"{self.endpoint}/{self.image.id}/change/")
        sleep(2)
        
        # Check if image is displayed in detail view
        image_elem = self.get_selenium_elems(
            {
                "image": f"img[src*='{self.image.image.url}']",
            }
        )["image"]
        self.assertTrue(image_elem, "Image not found in detail view")
        