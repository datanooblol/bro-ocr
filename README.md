# bro-ocr

- lightweight pydantic wrapper for quick OCR prototyping
- aims to speed up your work on OCR with an llm-agnostic approach
- constructing prompts, extracting information, validating result schemas — plug bro-ocr into your pipeline and it's handled

## the problem

every OCR-with-LLM project ends up hand-rolling the same three things: crop the region you care about, describe what you want back as a schema, then validate whatever JSON the model hands back. bro-ocr turns that into two objects instead of a pile of copy-pasted glue code — and it never locks you into a specific LLM provider.

## two objects you need to know

**`Template`** — serves as data model and configuration.

- an image has a size (`w`, `h`) and a list of `patches` (regions of interest)
- each `Patch` is a bounding box (`x`, `y`, `w`, `h`) plus its own `schemas` and an optional `instruction`
- each `Schema` is one field to extract — a `field` name, a `dtype`, and an optional per-field `instruction`

it's just data. build it once, reuse it for every document of that layout.

**`SchemaConverter`** — integrates with `Template` to create a dynamic pydantic data model, usable as both a schema builder and a schema validator.

- `from_single` — exactly one field (e.g. `total_amount: float`)
- `from_object` — a flat group of fields (e.g. `year`, `month`, `day`)
- `from_list` — a repeating group wrapped in a list (e.g. line `items`)

same model, two jobs: dump `.model_json_schema()` into your prompt so the LLM knows the shape you want back, then call `.model_validate_json(...)` on the response to make sure it actually came back that shape.

## install

pre-1.0, not on PyPI yet. clone it and install editable:

```bash
uv pip install -e .
```

## quickstart

define a patch and its schema:

```python
from bro_ocr.core.template import Dtype, Patch, Schema, SchemaType, Template

total_amount = Patch(
    name="total_amount",
    x=455, y=564, w=86, h=25,
    schema_type=SchemaType.SINGLE,
    schemas=[Schema(field="total_amount", dtype=Dtype.FLOAT)],
    instruction="amount is in float",
)

template = Template(name="invoice", w=578, h=750, patches=[total_amount])
```

turn it into a pydantic model, use it both ways:

```python
from bro_ocr.utils.conversion import SchemaConverter as sc

model = sc.from_single(total_amount.name, total_amount.schemas)

# 1. shape your prompt
model.model_json_schema()

# 2. validate what the LLM sent back
model.model_validate_json('{"total_amount": 551.56}')
```

`from_object` (flat group of fields) and `from_list` (repeating rows) work the same way. See [`notebooks/dev.ipynb`](notebooks/dev.ipynb) for a full invoice walkthrough covering all three `SchemaType`s, cropping patches out of a real image with `cv2`, and a worked example calling a vision model over AWS Bedrock.

## bring your own LLM

bro-ocr doesn't ship an LLM client and never will — that's the agnostic part. it preps the region, builds the schema, validates the response. wiring up OpenAI, Anthropic, Bedrock, a local VLM, whatever — that's on you, and it's about 20 lines (see the notebook for one way to do it).

## status

early days — `Template` + `SchemaConverter` is the whole lite core for now. more pieces (prompt packing, provider adapters, etc.) land later as opt-in extras without touching this base.

## license

Apache 2.0
