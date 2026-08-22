import pytest
from pydantic import ValidationError

from bro_ocr.core.template import Dtype, Patch, Schema, SchemaType, Template


def test_dtype_values():
    assert Dtype.STRING == "string"
    assert Dtype.INTEGER == "integer"
    assert Dtype.FLOAT == "float"
    assert Dtype.BOOLEAN == "boolean"
    assert Dtype.DATE == "date"
    assert Dtype.DATETIME == "datetime"


def test_schema_instruction_defaults_to_none():
    schema = Schema(field="total_amount", dtype=Dtype.FLOAT)
    assert schema.instruction is None


def test_schema_rejects_invalid_dtype():
    with pytest.raises(ValidationError):
        Schema(field="total_amount", dtype="not_a_dtype")


def test_patch_holds_its_schemas():
    patch = Patch(
        name="total_amount",
        x=455,
        y=564,
        w=86,
        h=25,
        schema_type=SchemaType.SINGLE,
        schemas=[Schema(field="total_amount", dtype=Dtype.FLOAT)],
    )
    assert patch.instruction is None
    assert len(patch.schemas) == 1
    assert patch.schema_type == SchemaType.SINGLE


def test_template_collects_patches():
    patch = Patch(
        name="total_amount",
        x=0,
        y=0,
        w=1,
        h=1,
        schema_type=SchemaType.SINGLE,
        schemas=[Schema(field="total_amount", dtype=Dtype.FLOAT)],
    )
    template = Template(name="invoice", w=578, h=750, patches=[patch])
    assert template.instruction is None
    assert len(template.patches) == 1


def test_template_requires_patches_field():
    with pytest.raises(ValidationError):
        Template(name="invoice", w=578, h=750)
