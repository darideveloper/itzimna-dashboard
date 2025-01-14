from time import sleep

from django.test import LiveServerTestCase
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils import test_data
from utils.automation import get_selenium_elems


class PropertyAdminTestCase(LiveServerTestCase):
    
    def setUp(self):
        
        # Create admin user
        self.admin_user, self.admin_pass, _ = test_data.create_admin_user()
        
        # Set endpoint
        self.endpoint = "/admin/properties/property/add/"
        
        self.__setup_selenium__()
        self.__login__()
        
    def tearDown(self):
        """ Close selenium """
        try:
            self.driver.quit()
        except Exception:
            pass

    def __setup_selenium__(self):
        """ Setup and open selenium browser """
        
        chrome_options = Options()
        if settings.TEST_HEADLESS:
            chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(5)
    
    def __login__(self):
        """ Login and load main page """
        
        # Load login page and get fields
        self.driver.get(f"{self.live_server_url}/admin/")
        sleep(2)
        selectors_login = {
            "username": "input[name='username']",
            "password": "input[name='password']",
            "submit": "button[type='submit']",
        }
        fields_login = get_selenium_elems(self.driver, selectors_login)

        fields_login["username"].send_keys(self.admin_user)
        fields_login["password"].send_keys(self.admin_pass)
        fields_login["submit"].click()

        # Wait after login
        sleep(3)
        
        # Open page
        url = f"{self.live_server_url}{self.endpoint}"
        print(f">>>>>{url}")
        self.driver.get(url)
        sleep(1)
        
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