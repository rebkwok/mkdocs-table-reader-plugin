"""
Note that pytest offers a `tmp_path`. 
You can reproduce locally with

```python
%load_ext autoreload
%autoreload 2
import os
import tempfile
import shutil
from pathlib import Path
tmp_path = Path(tempfile.gettempdir()) / 'pytest-table-builder'
if os.path.exists(tmp_path):
    shutil.rmtree(tmp_path)
os.mkdir(tmp_path)
```
"""

import re
import os
import shutil
import logging
from click.testing import CliRunner
from mkdocs.__main__ import build_command


def setup_clean_mkdocs_folder(mkdocs_yml_path, output_path):
    """
    Sets up a clean mkdocs directory
    
    outputpath/testproject
    ├── docs/
    └── mkdocs.yml
    
    Args:
        mkdocs_yml_path (Path): Path of mkdocs.yml file to use
        output_path (Path): Path of folder in which to create mkdocs project
        
    Returns:
        testproject_path (Path): Path to test project
    """

    testproject_path = output_path / "testproject"

    # Create empty 'testproject' folder
    if os.path.exists(testproject_path):
        logging.warning(
            """This command does not work on windows. 
        Refactor your test to use setup_clean_mkdocs_folder() only once"""
        )
        shutil.rmtree(testproject_path)

    # Copy correct mkdocs.yml file and our test 'docs/'
    shutil.copytree(
        os.path.join(os.path.dirname(mkdocs_yml_path), "docs"),
        testproject_path / "docs",
    )
    if os.path.exists(os.path.join(os.path.dirname(mkdocs_yml_path), "assets")):
        shutil.copytree(
            os.path.join(os.path.dirname(mkdocs_yml_path), "assets"),
            testproject_path / "assets",
        )
    shutil.copyfile(mkdocs_yml_path, testproject_path / "mkdocs.yml")

    return testproject_path


def build_docs_setup(testproject_path):
    """
    Runs the `mkdocs build` command
    
    Args:
        testproject_path (Path): Path to test project
    
    Returns:
        command: Object with results of command
    """

    cwd = os.getcwd()
    os.chdir(testproject_path)

    try:
        run = CliRunner().invoke(build_command)
        os.chdir(cwd)
        return run
    except:
        os.chdir(cwd)
        raise



def test_table_output(tmp_path):

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/basic_setup/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    index_file = tmp_proj / "site/index.html"
    assert index_file.exists(), f"{index_file} does not exist"

    # Make sure with markdown tag has the output
    page_with_tag = tmp_proj / "site/page_read_csv.html"
    contents = page_with_tag.read_text()
    assert re.search(r"531456", contents)

    # Make sure with markdown tag has the output
    page_with_tag = tmp_proj / "site/page_read_txt.html"
    contents = page_with_tag.read_text()
    assert re.search(r"531456", contents)

    # Make sure with markdown tag has the output
    page_with_tag = tmp_proj / "site/page_read_excel.html"
    contents = page_with_tag.read_text()
    assert re.search(r"531456", contents)

    # Make sure with markdown tag has the output
    page_with_tag = tmp_proj / "site/page_read_fwf.html"
    contents = page_with_tag.read_text()
    assert re.search(r"35000", contents)
    assert re.search(r"Audi A4", contents)

    # Make sure with markdown tag has the output
    page_with_tag = tmp_proj / "site/page_read_yaml.html"
    contents = page_with_tag.read_text()
    assert re.search(r"531456", contents)
    assert re.search(r"table1", contents)

    # Make sure with markdown tag has the output
    page_with_tag = tmp_proj / "site/page_read_json.html"
    contents = page_with_tag.read_text()
    assert re.search(r"1234json", contents)

    # Make sure multiple tags are supported
    page_with_tag = tmp_proj / "site/page_read_two_csv.html"
    contents = page_with_tag.read_text()
    assert re.search(r"table1", contents)
    assert re.search(r"table2", contents)


def test_compatibility_macros_plugin(tmp_path):

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/basic_setup/mkdocs_w_macros_wrong_order.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 1, "'mkdocs build' command should have failed"

    # Make sure correct error is raised
    assert (
        "[table-reader]: Incompatible plugin order:"
        in result.output
    )

    # With correct order, no error
    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/basic_setup/mkdocs_w_macros.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command should have succeeded"

def test_compatibility_markdownextradata(tmp_path):

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/markdownextradata/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    index_file = tmp_proj / "site/index.html"
    assert index_file.exists(), f"{index_file} does not exist"

    # Make sure with markdown tag has the output
    page_with_tag = tmp_proj / "site/index.html"
    contents = page_with_tag.read_text()
    # Make sure the table is inserted
    assert re.search(r"531456", contents)
    # Make sure the extradata 'web' is inserted
    assert re.search(r"www.example.com", contents)

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/markdownextradata/mkdocs_w_markdownextradata_wrong_order.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 1, "'mkdocs build' command should have failed"

    # Make sure correct error is raised
    assert (
        "[table-reader]: Incompatible plugin order:"
        in result.output
    )

    # With correct order, no error
    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/markdownextradata/mkdocs_w_markdownextradata.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command should have succeeded"


def test_datapath_1(tmp_path):

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/datapathproject/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    # Make sure the basic_table.csv is inserted
    page_with_tag = tmp_proj / "site/index.html"
    contents = page_with_tag.read_text()
    assert re.search(r"531456", contents)

    # Make sure the basic_table2.csv is inserted
    page_with_tag = tmp_proj / "site/page2.html"
    contents = page_with_tag.read_text()
    assert re.search(r"539956", contents)


def test_datapath_trailing(tmp_path):

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/datapathproject/mkdocs_trailingslash.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    # Make sure the basic_table.csv is inserted
    page_with_tag = tmp_proj / "site/index.html"
    contents = page_with_tag.read_text()
    assert re.search(r"531456", contents)

    # Make sure the basic_table2.csv is inserted
    page_with_tag = tmp_proj / "site/page2.html"
    contents = page_with_tag.read_text()
    assert re.search(r"539956", contents)


def test_datapath_with_spaces(tmp_path):

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/data_path_with_space/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    # Make sure the basic_table.csv is inserted
    page_with_tag = tmp_proj / "site/index.html"
    contents = page_with_tag.read_text()
    assert re.search(r"531456", contents)


def test_tablepath_with_spaces(tmp_path):

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/table_path_with_space/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    # Make sure the basic_table.csv is inserted
    page_with_tag = tmp_proj / "site/index.html"
    contents = page_with_tag.read_text()
    assert re.search(r"531456", contents)


def test_using_docs_dir(tmp_path):

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/using_docs_dir/mkdocs.yml", tmp_path
    )

    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    # Make sure the basic_table.csv is inserted
    page_with_tag = tmp_proj / "site/index.html"
    contents = page_with_tag.read_text()
    assert re.search(r"531456", contents)


def test_wrong_path(tmp_path):

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/wrongpath/mkdocs.yml", tmp_path
    )
    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 1, "'mkdocs build' command failed"
    assert "[table-reader-plugin]: File does not exist" in str(result.exception)
    assert "non_existing_table.csv" in str(result.exception)


def test_multiple_data_paths(tmp_path):

    tmp_proj = setup_clean_mkdocs_folder(
        "tests/fixtures/multiplepaths/mkdocs.yml", tmp_path
    )
    print(tmp_proj)
    result = build_docs_setup(tmp_proj)
    assert result.exit_code == 0, "'mkdocs build' command failed"

    page_with_table1 = tmp_proj / "site/table1/index.html"
    contents = page_with_table1.read_text()
    # Make sure table1.csv is inserted from the base path
    assert re.search(r"111111", contents)
    
    page_with_table2= tmp_proj / "site/table2/index.html"
    contents = page_with_table2.read_text()
    # Make sure table2.csv is inserted from the path "docs"
    assert re.search(r"222222", contents)

    page_with_table3 = tmp_proj / "site/table3/index.html"
    contents = page_with_table3.read_text()
    # Make sure the table3.csv is inserted from path "tables"
    assert re.search(r"333333", contents)

    page_with_no_tables = tmp_proj / "site/no_tables/index.html"
    contents = page_with_no_tables.read_text()
    # A page with no tables is rendered correctly
    assert re.search(r"This is a page with no tables", contents)
