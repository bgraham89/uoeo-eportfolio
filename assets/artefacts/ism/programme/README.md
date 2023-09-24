# README

## About

The purpose of this application, is to give a means to create a digital attack tree. The `main.py` file consists of three main capabilities:

1. The application can parse data to be represented as attack tree.
2. The application can be used to tag threats with threat metrics.
3. The application can be used to tag threat categories with aggregational threat metrics.
4. The aqpplication can be used to create a visual representation of the attack tree.

The main script can simply be run using:

`python main.py`

## STIX

The `main.py` application can parse data in STIX (Structured Threat Information Expression) format, represented in JSON. STIX is a language and serialisation format used to exhange cyber threat intelligence (CTI). More information can be found [here](https://oasis-open.github.io/cti-documentation/stix/intro). The STIX 2.1 specification has been included in the project folder aswell for reference.

### grouper and attack-pattern entities

When building an attack tree, the parser specifically looks for `grouper` and `attack-pattern` objects, which it interprets as threat catageories, and threats. `grouper` objects take the `object_refs` keyword to map directly to `attack-patterns`. Threat nesting can be achieved too using the `object_refs` keyword in an `attack-pattern`, but please note that this use case is technically an extension of STIX.

### STIX Validation

The `STIX_validation.py` script may be run from the command line in order to validate that a JSON file conforms to the STIX specification. It makes use of the `stix2validator` external library, that needs to be installed beforehand. To install it, run: 

`pip install stix2-validator`

Once the library is install, run the validator using:

`python ./STIX_validation.py`

It's recommended to store the JSON file in the `./STIX/` directory. Once the script has started, you will be prompted for the path to the JSON file.

### UUID

STIX requires each object to have it's own UUID idenitifier. For convenience, the `UUID_gen.py` script can be used to generate these if required. The UUID specification has been included in the project aswell for reference.

## Mermaid

The `main.py` plotter outputs a markdown file containing Mermaid syntax, which naturally renders in many markdown preview tools., such as the markdown previewer used on [GitHub](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams).

### Visual Studio Code Preview 

In order to preview Mermaid diagrams in Visual Studio Code, the `bpruitt-goddard.mermaid-markdown-syntax-highlighting` extension can be used, which gives Markdown file a right click option to preview them.

## Tagging

When tagging a threat or threat category, the object can be referenced using it's `name` property. A tag must consist of two parts: a keyword and a value. For example, the keyword `probability` might be used to tag a threat, with a value of `likely`, or `20%`. There is no strict format requirements for the values; they may be quantitative or qualitative. To view the tag on a diagram, the option to add detail is given when creating the diagram, where a keyword of a tag can be provided.

## Examples

Examples can be found in the `./Diagrams/` directory.