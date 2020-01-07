import subprocess
from documentation_generator import get_documentation, dump_documentation

# Generate docs for the module
docs = get_documentation("ftools")

# Make sure dependencies are installed for docs_src
subprocess.run(["yarn"], cwd="docs_src")

# Save it to docs.json
with open("docs_src/src/docs.json", "w+") as file:
    dump_documentation(docs, file)

subprocess.run(["yarn", "build"], cwd="docs_src")
