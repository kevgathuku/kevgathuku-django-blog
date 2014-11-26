from .base import FunctionalTest


class ContactPageTest(FunctionalTest):

    def test_cannot_submit_empty_contact_form(self):
        # A user navigates to the contact page
        self.browser.get(self.live_server_url + '/contact/')

        # The user tries to submit an empty contact form
        self.browser.find_element_by_id('name').send_keys('\n')
        self.browser.find_element_by_id('email').send_keys('\n')
        self.browser.find_element_by_id('message').send_keys('')
        self.browser.find_element_by_id('name').submit()

        # She gets an error informing her that the form must be filled in
        form = self.browser.find_element_by_tag_name('form')
        errors = form.find_elements_by_tag_name('p')

        self.assertIn("Please enter your name.", [msg.text for msg in errors])
        self.assertIn(
            "Please enter your email address.",
            [msg.text for msg in errors])
        self.assertIn("Please enter a message.", [msg.text for msg in errors])

    def test_submits_contact_form_successfully(self):
        # A user navigates to the contact page
        self.browser.get(self.live_server_url + '/contact/')

        # She submits the form correctly
        self.browser.find_element_by_id('name').send_keys('My name')
        self.browser.find_element_by_id('email').send_keys('name@example.com')
        self.browser.find_element_by_id('message').send_keys('Hi Kevin')
        self.browser.find_element_by_id('name').submit()

        success_text = self.browser.find_element_by_class_name(
            'alert-success').text
        self.assertIn("Thanks. Your message has been sent.", success_text)
