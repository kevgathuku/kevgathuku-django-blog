from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_home_page(self):
        self.browser.get(self.live_server_url)

        self.assertIn("Kevin Ndung'u", self.browser.title)
        self.assertIn("Home", self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Kevin', header_text)

    def test_layout_and_styling(self):
        # Home page styling
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        header = self.browser.find_element_by_tag_name('h1')
        self.assertAlmostEqual(
            header.location['x'] + header.size['width'] / 2,
            512,
            delta=5
        )

        footer = self.browser.find_element_by_tag_name('footer')
        links = footer.find_elements_by_tag_name('a')
        twitter_link = links[0]

        self.assertIn(
            'https://twitter.com/kevgathuku',
            twitter_link.get_attribute('href'))
