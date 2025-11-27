import unittest

from core import get_from_collection, set_in_collection


class DictUtilsTest(unittest.TestCase):
    def setUp(self):
        self.test_data = {
            "name": {
                "first": "Akido",
                "second": "Rayan"
            },
            "course": [
                "math",
                "physic"
            ]
        }

    # Tests pour get_from_collection
    def test_get_from_collection_return_the_correct_value(self):
        self.assertEqual(get_from_collection(self.test_data, "name.first"), "Akido")
        self.assertEqual(get_from_collection(self.test_data, "course.0"), "math")
        self.assertEqual(get_from_collection(self.test_data, "course.1"), "physic")

    def test_get_from_collection_returns_none_for_invalid_path(self):
        self.assertIsNone(get_from_collection(self.test_data, "name.invalid"))
        self.assertIsNone(get_from_collection(self.test_data, "invalid.path"))
        self.assertIsNone(get_from_collection(self.test_data, "course.10"))

    def test_get_from_collection_returns_none_for_empty_path(self):
        self.assertIsNone(get_from_collection(self.test_data, ""))
        self.assertIsNone(get_from_collection(self.test_data, "   "))

    def test_get_from_collection_raises_type_error_for_non_string_path(self):
        with self.assertRaises(TypeError):
            get_from_collection(self.test_data, 123)
        with self.assertRaises(TypeError):
            get_from_collection(self.test_data, None)
        with self.assertRaises(TypeError):
            get_from_collection(self.test_data, ["name", "first"])

    def test_get_from_collection_with_nested_lists(self):
        data = {"items": [["a", "b"], ["c", "d"]]}
        self.assertEqual(get_from_collection(data, "items.0.1"), "b")
        self.assertEqual(get_from_collection(data, "items.1.0"), "c")

    def test_get_from_collection_with_tuple(self):
        data = {"coords": (10, 20, 30)}
        self.assertEqual(get_from_collection(data, "coords.0"), 10)
        self.assertEqual(get_from_collection(data, "coords.2"), 30)

    def test_get_from_collection_returns_dict_or_list(self):
        self.assertEqual(get_from_collection(self.test_data, "name"), {"first": "Akido", "second": "Rayan"})
        self.assertEqual(get_from_collection(self.test_data, "course"), ["math", "physic"])

    # Tests pour set_in_collection
    def test_set_in_collection_can_set_value(self):
        value = "LD"
        self.assertTrue(set_in_collection(self.test_data, "name.second", value))
        self.assertEqual(get_from_collection(self.test_data, "name.second"), value)

    def test_set_in_collection_can_set_value_in_list(self):
        value = "chemistry"
        self.assertTrue(set_in_collection(self.test_data, "course.0", value))
        self.assertEqual(get_from_collection(self.test_data, "course.0"), value)

    def test_set_in_collection_can_create_new_key(self):
        value = "Doe"
        self.assertTrue(set_in_collection(self.test_data, "name.last", value))
        self.assertEqual(get_from_collection(self.test_data, "name.last"), value)

    def test_set_in_collection_returns_false_for_invalid_path(self):
        self.assertFalse(set_in_collection(self.test_data, "invalid.path.deep", "value"))
        self.assertFalse(set_in_collection(self.test_data, "course.10", "value"))

    def test_set_in_collection_returns_false_for_empty_path(self):
        self.assertFalse(set_in_collection(self.test_data, "", "value"))
        self.assertFalse(set_in_collection(self.test_data, "   ", "value"))

    def test_set_in_collection_raises_type_error_for_non_string_path(self):
        with self.assertRaises(TypeError):
            set_in_collection(self.test_data, 123, "value")
        with self.assertRaises(TypeError):
            set_in_collection(self.test_data, None, "value")
        with self.assertRaises(TypeError):
            set_in_collection(self.test_data, ["name", "first"], "value")

    def test_set_in_collection_with_nested_structure(self):
        data = {"level1": {"level2": {"level3": "old"}}}
        self.assertTrue(set_in_collection(data, "level1.level2.level3", "new"))
        self.assertEqual(get_from_collection(data, "level1.level2.level3"), "new")

    def test_set_in_collection_with_mixed_dict_and_list(self):
        data = {"users": [{"name": "Alice"}, {"name": "Bob"}]}
        self.assertTrue(set_in_collection(data, "users.0.name", "Charlie"))
        self.assertEqual(get_from_collection(data, "users.0.name"), "Charlie")

    def test_set_in_collection_returns_false_on_type_mismatch(self):
        # Essayer de set sur un type non-indexable
        data = {"value": "string"}
        self.assertFalse(set_in_collection(data, "value.invalid", "test"))

    def test_set_in_collection_with_numeric_string_key(self):
        # Test avec une clé qui est un string numérique dans un dict
        data = {"items": {"5": "value5", "10": "value10"}}
        self.assertTrue(set_in_collection(data, "items.5", "new_value"))
        self.assertEqual(get_from_collection(data, "items.5"), "new_value")

    def test_integration_get_and_set(self):
        # Test d'intégration : set puis get
        original = get_from_collection(self.test_data, "name.first")
        new_value = "NewName"
        set_in_collection(self.test_data, "name.first", new_value)
        self.assertEqual(get_from_collection(self.test_data, "name.first"), new_value)
        self.assertNotEqual(get_from_collection(self.test_data, "name.first"), original)