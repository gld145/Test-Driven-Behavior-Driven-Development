######################################################################
# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################
"""
Product API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
  codecov --token=$CODECOV_TOKEN

  While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_service.py:TestProductService
"""
import logging
import os
from decimal import Decimal
from unittest import TestCase

from service import app
from service.common import status
from service.models import Product, db, init_db
from tests.factories import ProductFactory

# Disable all but critical errors during normal test run
# uncomment for debugging failing tests
# logging.disable(logging.CRITICAL)

# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)
BASE_URL = "/products"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods


class TestProductRoutes(TestCase):
    """Product Service tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    ############################################################
    # Utility function to bulk create products
    ############################################################
    def _create_products(self, count: int = 1) -> list:
        """Factory method to create products in bulk"""
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            response = self.client.post(BASE_URL, json=test_product.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test product",
            )
            new_product = response.get_json()
            test_product.id = new_product["id"]
            products.append(test_product)
        return products

    ############################################################
    #  T E S T   C A S E S
    ############################################################
    def test_index(self):
        """It should return the index page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b"Product Catalog Administration", response.data)

    def test_health(self):
        """It should be healthy"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["message"], "OK")

    # ----------------------------------------------------------
    # TEST CREATE
    # ----------------------------------------------------------
    def test_create_product(self):
        """It should Create a new Product"""
        test_product = ProductFactory()
        logging.debug("Test Product: %s", test_product.serialize())
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_product = response.get_json()
        self.assertEqual(new_product["name"], test_product.name)
        self.assertEqual(new_product["description"], test_product.description)
        self.assertEqual(Decimal(new_product["price"]), test_product.price)
        self.assertEqual(new_product["available"], test_product.available)
        self.assertEqual(new_product["category"], test_product.category.name)

        #
        # Uncomment this code once READ is implemented
        #

        # # Check that the location header was correct
        # response = self.client.get(location)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # new_product = response.get_json()
        # self.assertEqual(new_product["name"], test_product.name)
        # self.assertEqual(new_product["description"], test_product.description)
        # self.assertEqual(Decimal(new_product["price"]), test_product.price)
        # self.assertEqual(new_product["available"], test_product.available)
        # self.assertEqual(new_product["category"], test_product.category.name)

    def test_create_product_with_no_name(self):
        """It should not Create a Product without a name"""
        product = self._create_products()[0]
        new_product = product.serialize()
        del new_product["name"]
        logging.debug("Product no name: %s", new_product)
        response = self.client.post(BASE_URL, json=new_product)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_no_content_type(self):
        """It should not Create a Product with no Content-Type"""
        response = self.client.post(BASE_URL, data="bad data")
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_product_wrong_content_type(self):
        """It should not Create a Product with wrong Content-Type"""
        response = self.client.post(BASE_URL, data={}, content_type="plain/text")
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    #
    # ADD YOUR TEST CASES HERE
    #
    def test_get_product(self):
        """It should Get a single Product"""
        # Step 1: Create a product
        # Create one product and assign it
        test_product = self._create_products(1)[0]

        # Step 2: Make a GET request to retrieve the product
        response = self.client.get(f"{BASE_URL}/{test_product.id}")

        # Step 3: Assert that the response status is HTTP_200_OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Step 4: Verify that the returned data matches the created product
        data = response.get_json()
        self.assertEqual(data["id"], test_product.id)
        self.assertEqual(data["name"], test_product.name)
        self.assertEqual(data["description"], test_product.description)
        self.assertEqual(Decimal(data["price"]), test_product.price)
        self.assertEqual(data["available"], test_product.available)
        self.assertEqual(data["category"], test_product.category.name)

    def test_get_product_not_found(self):
        """It should return 404 NOT FOUND for a non-existent Product"""

        invalid_id = 0  # Define a known invalid ID
        response = self.client.get(f"{BASE_URL}/{invalid_id}")

        # Assert that the response returns 404 NOT FOUND
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Debugging: Print response details
        print(f"🔹 GET Request for non-existent ID {invalid_id}")
        print(f"🔹 Response Status: {response.status_code}")
        print(f"🔹 Response Data: {response.get_json()}")

        # Step 3: Verify that the response status is HTTP_404_NOT_FOUND
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Step 4: Check that an error message is returned
        data = response.get_json()
        self.assertIn("message", data)  # Ensure 'message' key is present
        self.assertEqual(
            data["message"], f"Product with id '{invalid_id}' was not found."
        )

    ######################################################################
    # Utility functions
    ######################################################################

    def get_product_count(self):
        """save the current number of products"""
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        # logging.debug("data = %s", data)
        return len(data)
        ######################################################################

    # UPDATE AN EXISTING PRODUCT
    ######################################################################
    @app.route("/products/<int:product_id>", methods=["PUT"])
    def update_products(product_id):
        """
        Update a Product

        This endpoint will update a Product based the body that is posted
        """
        app.logger.info("Request to Update a product with id [%s]", product_id)
        check_content_type("application/json")

        product = Product.find(product_id)
        if not product:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Product with id '{product_id}' was not found.",
            )

        product.deserialize(request.get_json())
        product.id = product_id
        product.update()
        return product.serialize(), status.HTTP_200_OK

        ######################################################################

    # DELETE A PRODUCT
    ######################################################################

    @app.route("/products/<int:product_id>", methods=["DELETE"])
    def delete_products(product_id):
        """
        Delete a Product

        This endpoint will delete a Product based the id specified in the path
        """
        app.logger.info("Request to Delete a product with id [%s]", product_id)

        product = Product.find(product_id)
        if product:
            product.delete()

        return "", status.HTTP_204_NO_CONTENT

    ######################################################################
    # LIST PRODUCTS
    ######################################################################

    @app.route("/products", methods=["GET"])
    def list_products():
        """Returns a list of Products"""
        app.logger.info("Request to list Products...")

        products = Product.all()

        results = [product.serialize() for product in products]
        app.logger.info("[%s] Products returned", len(results))
        return results, status.HTTP_200_OK

        ######################################################################

    # LIST PRODUCTS
    ######################################################################
    @app.route("/products", methods=["GET"])
    def list_products():
        """Returns a list of Products"""
        app.logger.info("Request to list Products...")

        products = []
        name = request.args.get("name")
        category = request.args.get("category")
        available = request.args.get("available")

        if name:
            app.logger.info("Find by name: %s", name)
            products = Product.find_by_name(name)
        elif category:
            app.logger.info("Find by category: %s", category)
            # create enum from string
            category_value = getattr(Category, category.upper())
            products = Product.find_by_category(category_value)
        elif available:
            app.logger.info("Find by available: %s", available)
            # create bool from string
            available_value = available.lower() in ["true", "yes", "1"]
            products = Product.find_by_availability(available_value)
        else:
            app.logger.info("Find all")
            products = Product.all()

        results = [product.serialize() for product in products]
        app.logger.info("[%s] Products returned", len(results))
        return results, status.HTTP_200_OK
