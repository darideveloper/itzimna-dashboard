from time import sleep

from utils.automation import get_selenium_elems
from core.test_base.test_admin import TestAdminSeleniumBase, TestAdminBase
from core.test_base.test_models import TestPropertiesModelsBase


class CompanyAdminTestCase(TestAdminBase):
    """Testing company admin"""

    def setUp(self):
        super().setUp()
        self.endpoint = "/admin/properties/company/"

    def test_search_bar(self):
        """Validate search bar working"""

        self.submit_search_bar(self.endpoint)


class LocationAdminTestCase(TestAdminBase):
    """Testing location admin"""

    def setUp(self):
        super().setUp()
        self.endpoint = "/admin/properties/location/"

    def test_search_bar(self):
        """Validate search bar working"""

        self.submit_search_bar(self.endpoint)


class CategoryAdminTestCase(TestAdminBase):
    """Testing category admin"""

    def setUp(self):
        super().setUp()
        self.endpoint = "/admin/properties/category/"

    def test_search_bar(self):
        """Validate search bar working"""

        self.submit_search_bar(self.endpoint)


class TagAdminTestCase(TestAdminBase):
    """Testing tag admin"""

    def setUp(self):
        super().setUp()
        self.endpoint = "/admin/properties/tag/"

    def test_search_bar(self):
        """Validate search bar working"""

        self.submit_search_bar(self.endpoint)


class ShortDescriptionAdminTestCase(TestAdminBase):
    """Testing short description admin"""

    def setUp(self):
        super().setUp()
        self.endpoint = "/admin/properties/shortdescription/"

    def test_search_bar(self):
        """Validate search bar working"""

        self.submit_search_bar(self.endpoint)


class SellerAdminTestCase(TestAdminBase):
    """Testing seller admin"""

    def setUp(self):
        super().setUp()
        self.endpoint = "/admin/properties/seller/"

    def test_search_bar(self):
        """Validate search bar working"""

        self.submit_search_bar(self.endpoint)


class PropertyAdminTestCase(TestAdminBase):
    """Testing property admin"""

    def setUp(self):
        super().setUp()
        self.endpoint = "/admin/properties/property/"

    def test_search_bar(self):
        """Validate search bar working"""

        self.submit_search_bar(self.endpoint)


class PropertyAdminTestCaseSelenium(TestAdminSeleniumBase):
    """Testing property admin with selenium"""

    def setUp(self):

        # Submit endpoint
        super().setUp("/admin/properties/property/add")

        self.markdown_selectors = {
            "tool_bar": ".editor-toolbar",
            "bold": 'a[title="Bold (Ctrl-B)"]',
            "editor": ".CodeMirror-scroll",
            "status_bar": ".editor-statusbar",
        }

    def test_markdown_editor_loaded(self):
        """Check if markdown is not allowed in google maps src"""

        elems = get_selenium_elems(self.driver, self.markdown_selectors)
        for elem_name, elem in elems.items():
            self.assertTrue(elem, f"Element {elem_name} not found")

    def test_no_markdown_in_google_maps_src(self):
        """
        Check if the editor is loaded with reference elements
        """

        # Add wrapper class to each markdown element
        wrapper_class = "field-google_maps_src"
        for elem_name, elem in self.markdown_selectors.items():
            self.markdown_selectors[elem_name] = f".{wrapper_class} {elem}"

        elems = get_selenium_elems(self.driver, self.markdown_selectors)
        for elem_name, elem in elems.items():
            self.assertIsNone(elem, f"Element {elem_name} found (should not be found)")


class PropertyImageAdminTestCase(TestAdminBase):
    """Testing property image admin"""

    def setUp(self):
        super().setUp()
        self.endpoint = "/admin/properties/propertyimage/"

    def test_search_bar(self):
        """Validate search bar working"""

        self.submit_search_bar(self.endpoint)


class PropertyImageAdminTestCaseSelenium(
    TestAdminSeleniumBase, TestPropertiesModelsBase
):
    """Testing property image admin with selenium"""

    def setUp(self):

        # Create image instance
        self.image = self.create_property_image()

        # Login
        super().setUp()

        self.endpoint = "/admin/properties/propertyimage"

    def test_image_list_view(self):
        """Check if image list view is loaded"""

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
        """Check if image detail view is loaded"""

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


class CompanyAdminTestCaseSelenium(TestAdminSeleniumBase, TestPropertiesModelsBase):
    """Testing company admin with selenium"""

    def setUp(self):

        # Create image instance
        self.company = self.create_company()

        # Login
        super().setUp()

        # Endpoints
        self.endpoint_list = "/admin/properties/company"
        self.endpoint_edit = f"{self.endpoint_list}/{self.company.id}/change/"

        # General selectors
        self.markdown_selectors = {
            "tool_bar": ".editor-toolbar",
            "bold": 'a[title="Bold (Ctrl-B)"]',
            "editor": ".CodeMirror-scroll",
            "status_bar": ".editor-statusbar",
        }

    def test_list_view_logos(self):
        """Check if logo images are displayed in list view"""

        # Submit endpoint
        self.set_page(self.endpoint_list)

        # Check if image is displayed in list view
        image_elem = self.get_selenium_elems(
            {
                "logo": f"img[src*='{self.company.logo.url}']",
            }
        )["logo"]
        self.assertTrue(image_elem, "Image not found in list view")

    def test_details_view_images(self):
        """Check if images (logo and banner) are displayed in detail view"""

        # Submit endpoint
        self.set_page(self.endpoint_edit)

        # Check if image is displayed in detail view
        image_elems = self.get_selenium_elems(
            {
                "logo": f"img[src*='{self.company.logo.url}']",
                "banner": f"img[src*='{self.company.banner.url}']",
            }
        )
        self.assertTrue(image_elems["logo"], "Image not found in detail view")
        self.assertTrue(image_elems["banner"], "Image not found in detail view")

    def test_details_view_markdown_editor_loaded(self):
        """Check if markdown is not allowed in google maps src"""

        self.set_page(self.endpoint_edit)

        elems = get_selenium_elems(self.driver, self.markdown_selectors)
        for elem_name, elem in elems.items():
            self.assertTrue(elem, f"Element {elem_name} not found")

    def test_details_view_no_markdown_in_google_maps_src(self):
        """
        Check if the editor is loaded with reference elements
        """

        self.set_page(self.endpoint_edit)

        # Add wrapper class to each markdown element
        wrapper_class = "field-google_maps_src"
        for elem_name, elem in self.markdown_selectors.items():
            self.markdown_selectors[elem_name] = f".{wrapper_class} {elem}"

        elems = get_selenium_elems(self.driver, self.markdown_selectors)
        for elem_name, elem in elems.items():
            self.assertIsNone(elem, f"Element {elem_name} found (should not be found)")
