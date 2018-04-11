from django.test import TestCase, Client
from django.urls import reverse
from openfoodfacts.models import Products, Categories, Substitutes, User
from openfoodfacts.forms import UserCreationForm


class IndexPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class LegalsPageTestCase(TestCase):
    def test_legals_page(self):
        response = self.client.get(reverse('openfoodfacts:legals'))
        self.assertEqual(response.status_code, 200)


class ContactsPageTestCase(TestCase):
    def test_contacts_page(self):
        response = self.client.get(reverse('openfoodfacts:contacts'))
        self.assertEqual(response.status_code, 200)


class DetailPageTestCase(TestCase):
    def setUp(self):
        category = Categories.objects.create(category_name="Pâte à tartiner")
        nutella = Products.objects.create(
            id_product=1,
            product_name="nutella",
            category=category
            )
        self.product = Products.objects.get(product_name="nutella")

    #test that detail page returns a 200 if the item exists
    def test_detail_page_returns_200(self):
        product_id = self.product.id_product
        response = self.client.get(reverse('openfoodfacts:detail', args=(product_id,)))
        self.assertEqual(response.status_code, 200)

    #test that detail page returns a 404 if the item doesn't exists
    def test_detail_page_returns_404(self):
        product_id = self.product.id_product + 1
        response = self.client.get(reverse('openfoodfacts:detail', args=(product_id,)))
        self.assertEqual(response.status_code, 404)


class SearchPageTestCase(TestCase):
    def setUp(self):
        category = Categories.objects.create(category_name="Pâte à tartiner")
        Products.objects.create(
            id_product=1,
            product_name="nutella",
            category=category,
            nutriscore="c"
            )

        Products.objects.create(
            id_product=2,
            product_name="Nocciolata",
            category=category,
            nutriscore="a"
        )
        self.password = "1234abcd"
        self.user = User.objects.create_user(
            username="david",
            password=self.password,
            email="email@email.com")

        self.client = Client()
        self.origin = Products.objects.get(pk=1)
        self.replacement = Products.objects.get(pk=2)
        self.client.force_login(user=self.user)

    # test that detail page returns a 200 if the item exists
    def test_search_page_returns_200(self):
        response = self.client.get(reverse('openfoodfacts:search'), {"query": "nutella"})
        self.assertEqual(response.status_code, 200)

    # test that detail page returns a 200 if the item exists
    def test_search_page_returns_404(self):
        response = self.client.get(reverse('openfoodfacts:search'), {"query": "kiri"})
        self.assertEqual(response.status_code, 404)

    def test_search_replace_product(self):
        url = reverse('openfoodfacts:search') + '?query=nutella'
        self.client.post(url, {
            "origin": self.origin.id_product,
            "replacement": self.replacement.id_product,
            })

        self.assertTrue(Substitutes.objects.exists())


class RegisterTestPageCase(TestCase):
    def setUp(self):
        url = reverse('openfoodfacts:sign_up')
        data = {
            'username': 'john',
            'email': 'john@doe.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }

        self.home_url=(reverse('openfoodfacts:account'))
        self.response = self.client.post(url, data)

    def test_register_page_returns_200(self):
        response = self.client.get(reverse('openfoodfacts:sign_up'))
        self.assertEqual(response.status_code, 200)

    def test_registration(self):
        self.assertTrue(User.objects.exists())

    def test_csrf(self):
        response = self.client.get(reverse('openfoodfacts:sign_up'))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        response = self.client.get(reverse('openfoodfacts:sign_up'))
        form = response.context.get('form')
        self.assertIsInstance(form, UserCreationForm)

    def test_user_authentication(self):
        '''
        Create a new request to an arbitrary page.
        The resulting response should now have a `user` to its context,
        after a successful sign up.
        '''
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('openfoodfacts:sign_up')
        self.response = self.client.post(url, {})  # submit an empty dictionary

    def test_signup_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())


class LoginTestPageCase(TestCase):
    def setUp(self):
        self.username = "test"
        self.password = hash("1234abcd")
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_page(self):
        response = self.client.get(reverse('openfoodfacts:login'))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post(reverse('openfoodfacts:login'), {
            "username": self.username,
            "password": self.password,
            })
        self.assertEqual(response.status_code, 302)

    def test_login_fail_username(self):
        response = self.client.post(reverse('openfoodfacts:login'), {
            "username": ' ',
            "password": self.password,
            })
        self.assertEqual(response.status_code, 200)

    def test_login_fail_password(self):
        response = self.client.post(reverse('openfoodfacts:login'), {
            "username": self.username,
            "password": 'defgzpzd,',
            })
        self.assertEqual(response.status_code, 200)

    def test_csrf(self):
        response = self.client.get(reverse('openfoodfacts:login'))
        self.assertContains(response, 'csrfmiddlewaretoken')


class AccountTestPageCase(TestCase):
    def setUp(self):
        url = reverse('openfoodfacts:account')
        self.data = {
            'username': 'john',
            'email': 'john@doe.com',
            'password': 'abcdef123456',
        }
        self.response = self.client.post(url, self.data)
        self.user = User.objects.create_user(**self.data)

    def test_account_page_returns_200(self):
        self.client.login(**self.data)
        response = self.client.get(reverse('openfoodfacts:account'))
        self.assertEqual(response.status_code, 200)

    def test_account_page_redirects(self):
        response = self.client.get(reverse('openfoodfacts:account'))
        self.assertEqual(response.status_code, 302)


class SavedTestPageCase(TestCase):
    def setUp(self):
        url = reverse('openfoodfacts:saved')
        self.data = {
            'username': 'john',
            'email': 'john@doe.com',
            'password': 'abcdef123456',
        }
        self.response = self.client.post(url, self.data)

        self.user = User.objects.create_user(**self.data)
        category = Categories.objects.create(category_name="Pâte à tartiner")

        origin = Products.objects.create(
            id_product=1,
            product_name="nutella",
            category=category
            )

        replacement = Products.objects.create(
            id_product=2,
            product_name="Nocciolata",
            category=category
        )

        Substitutes.objects.create(
            origin=origin,
            replacement=replacement,
            user=self.user)

        self.origin = Products.objects.get(pk=1)
        self.replacement = Products.objects.get(pk=2)

    def test_account_page_returns_200(self):
        self.client.login(**self.data)
        response = self.client.get(reverse('openfoodfacts:saved'))
        self.assertEqual(response.status_code, 200)

    def test_account_page_redirects(self):
        response = self.client.get(reverse('openfoodfacts:saved'))
        self.assertEqual(response.status_code, 302)

    def test_delete_substitute(self):
        self.client.login(**self.data)
        self.client.post(reverse('openfoodfacts:saved'), {
            "origin": self.origin.id_product,
            "replacement": self.replacement.id_product,
            })
        self.assertFalse(Substitutes.objects.exists())
