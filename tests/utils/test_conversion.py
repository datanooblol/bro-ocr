import pytest
from pydantic import ValidationError

from bro_ocr.core.template import Dtype, Schema
from bro_ocr.utils.conversion import SchemaConverter


def test_from_single_builds_model_with_one_field():
    model = SchemaConverter.from_single(
        "total_amount", [Schema(field="total_amount", dtype=Dtype.FLOAT)]
    )
    instance = model(total_amount=0.1)
    assert instance.total_amount == 0.1


def test_from_single_rejects_zero_schemas():
    with pytest.raises(ValueError):
        SchemaConverter.from_single("total_amount", [])


def test_from_single_rejects_multiple_schemas():
    schemas = [
        Schema(field="a", dtype=Dtype.STRING),
        Schema(field="b", dtype=Dtype.STRING),
    ]
    with pytest.raises(ValueError):
        SchemaConverter.from_single("name", schemas)


def test_from_object_builds_model_with_multiple_fields():
    schemas = [
        Schema(field="year", dtype=Dtype.INTEGER),
        Schema(field="month", dtype=Dtype.INTEGER),
        Schema(field="day", dtype=Dtype.INTEGER),
    ]
    model = SchemaConverter.from_object("invoice_date", schemas)
    instance = model(year=2025, month=5, day=10)
    assert (instance.year, instance.month, instance.day) == (2025, 5, 10)


def test_from_object_rejects_single_schema():
    with pytest.raises(ValueError):
        SchemaConverter.from_object("name", [Schema(field="a", dtype=Dtype.STRING)])


def test_from_list_wraps_items_under_name():
    schemas = [
        Schema(field="description", dtype=Dtype.STRING),
        Schema(field="amount", dtype=Dtype.FLOAT),
    ]
    model = SchemaConverter.from_list("items", schemas)
    instance = model(
        items=[
            {"description": "a", "amount": 1},
            {"description": "b", "amount": 2},
        ]
    )
    assert len(instance.items) == 2
    assert instance.items[0].description == "a"
    assert instance.items[0].amount == 1.0


def test_from_list_validates_nested_items():
    schemas = [Schema(field="amount", dtype=Dtype.FLOAT)]
    model = SchemaConverter.from_list("items", schemas)
    with pytest.raises(ValidationError):
        model(items=[{"amount": "not-a-float"}])


@pytest.mark.parametrize(
    "dtype,expected_type",
    [
        (Dtype.STRING, str),
        (Dtype.INTEGER, int),
        (Dtype.FLOAT, float),
        (Dtype.BOOLEAN, bool),
        (Dtype.DATE, str),
        (Dtype.DATETIME, str),
    ],
)
def test_dtype_map_covers_every_dtype(dtype, expected_type):
    model = SchemaConverter.from_single("x", [Schema(field="x", dtype=dtype)])
    assert model.model_fields["x"].annotation is expected_type
