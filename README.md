# Check Version

This action compares the version number from your working branch to the main branch.

The comparison follows the PEP 440 Version Identification and Dependency Specification.

More detailed information about the versions can be found [here](https://packaging.python.org/en/latest/specifications/version-specifiers/)

# Usage

<!-- start usage -->
```yaml
- name: Checkout main
  uses: actions/checkout@v4
  with:
    ref: 'main'
    path: 'main'

- name: Checkout current working branch
  uses: actions/checkout@v4
  with:
    path: 'branch'
    
- name: Compare versions
  # Don't run on main otherwise it will compare main with main
  if: ${{ github.ref != 'refs/heads/main' }} 
  id: version_comparison
  uses: khalford/check-version-action@main
  with:
    # Path to version file from project root
    path: "version.txt"
    
- name: Log Success
  if: ${{ steps.version_comparison.outputs.updated == "true" }}
  run: |
    echo "Version has been updated correctly!"
```
<!-- end usage -->

