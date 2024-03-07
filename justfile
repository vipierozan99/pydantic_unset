
test arg=".":
    FORCE_COLOR=1 BETTER_EXCEPTIONS=1 pytest tests -k {{arg}} --tb=short --show-capture stdout  --log-level=error --ignore ./database --ignore ./scripts

test_with_log arg=".":
    FORCE_COLOR=1 BETTER_EXCEPTIONS=1 pytest tests -k {{arg}} --tb=short --show-capture log --log-level=error --ignore ./database --ignore ./scripts
