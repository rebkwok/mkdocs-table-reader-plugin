---
hide:
  - navigation
---

# Customization

You can customize the resulting markdown tables! 

## Theory

Under the hood `mkdocs-table-reader-plugin` is basically doing:

```python
import pandas as pd
df = pd.read_csv('path_to_table.csv')
df.to_markdown(index=False, tablefmt='pipe')
```

Any keyword arguments you give to <code>\{\{ read_csv('path_to_your_table.csv') \}\}</code> will be matched and passed the corresponding [pandas.read_csv()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html) or 
[.to_markdown()](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_markdown.html) functions. 

Pandas's `.to_markdown()` uses the [tabulate](https://pypi.org/project/tabulate/) package and any keyword arguments that are passed to it. Tabulate in turn offers many customization options, see [library usage](https://github.com/astanin/python-tabulate#library-usage). 

## Aligning columns

Text columns will be aligned to the left [by default](https://github.com/astanin/python-tabulate#column-alignment), whilst columns which contain only numbers will be aligned to the right. You can override this behaviour using [tabulate](https://pypi.org/project/tabulate/)'s [custom column alignment](https://github.com/astanin/python-tabulate#custom-column-alignment). Example:

=== ":arrow_left: left"

    <code>\{\{ read_csv('tables/basic_table.csv', colalign=("left",)) \}\}</code>

    {{ read_csv('tables/basic_table.csv', colalign=("left",)) }}

=== ":left_right_arrow: center"

    <code>\{\{ read_csv('tables/basic_table.csv', colalign=("center",)) \}\}</code>

    {{ read_csv('tables/basic_table.csv', colalign=("center",)) }}

=== ":arrow_right: right"

    <code>\{\{ read_csv('tables/basic_table.csv', colalign=("right",)) \}\}</code>

    {{ read_csv('tables/basic_table.csv', colalign=("right",)) }}

## Sortable tables

If you use [mkdocs-material](https://squidfunk.github.io/mkdocs-material), you can configure [sortable tables](https://squidfunk.github.io/mkdocs-material/reference/data-tables/?h=tables#sortable-tables).


## Number formatting

You can use [tabulate](https://pypi.org/project/tabulate/)'s [number formatting](https://github.com/astanin/python-tabulate#number-formatting). Example:

=== ":zero:"

    <code>\{\{ read_fwf('tables/fixedwidth_table.txt', floatfmt=".0f") \}\}</code>

    {{ read_fwf('tables/fixedwidth_table.txt', floatfmt=".0f") }}

=== ":one:"

    <code>\{\{ read_fwf('tables/fixedwidth_table.txt', floatfmt=".1f") \}\}</code>

    {{ read_fwf('tables/fixedwidth_table.txt', floatfmt=".1f") }}

=== ":two:"

    <code>\{\{ read_fwf('tables/fixedwidth_table.txt', floatfmt=".2f") \}\}</code>

    {{ read_fwf('tables/fixedwidth_table.txt', floatfmt=".2f") }}

