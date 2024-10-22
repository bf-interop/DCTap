# BIG DCTAP

## Introduction
BIG has chosen to capture BIBFRAME application profiles using the [DC Tabular Application Profiles (DCTAP)](https://www.dublincore.org/specifications/dctap/), an application profile specification from DCMI, because it meets our two primary requirements. It is a low barrier format for creating and reading metadata application profiles, and it is structured in such a way that it can be converted relatively easily into RDF validation formats.

The tab delimited files available here conform to the DCTAP specification with minor caveats. The majority of the elements used in BIG DCTAP are formally defined in the DCTAP specification, but it is important to note we also have implemented an extension to support the conversion to [The Shapes Constraint Language](https://www.w3.org/TR/shacl/), a W3C specification designed to support validation of RDF.

### Official DCTAP Elements used in BIG DCTAP
* shapeID (identifier for the entity shape)
* shapeLabel (label for the entity shape)
* propertyID (official URI for the property used)
* propertyLabel (human readable label for the property in relation to the entity shape, e.g Work Title)
* valueShape (shape id for “embedded” shapes, e.g. a Work shape can link to a Title shape)
* mandatory (true if we want to generate a Violation or Warning note)
* severity (to record whether we want a Violation or Warning note)
* valueNodeType (to record whether the value of the property should be an IRI, bnode, or literal)
* repeatable (true if repeatable, false if not repeatable)
* note (the value of the Violation or Warning Note for a given property)

### BIG DCTAP Extension Elements
* target (used to record the class type/s for the entity shape)

## Current and Future Work
DCTAP has been created for Monographs and Serials, we will iterate on these, and DCTAP for other resource types will gradually be added.

## Versioning
Versioning of the DCTAP and SHACL will be managed globally at the repository level using GitHub versioning tags and release features. For each version, reports are available to describe exactly what was changed between versions, e.g. https://github.com/bf-interop/DCTap/releases/tag/v0.1.0. Semantic versioning will be supported with version numbering; any major changes, especially breaking changes, will trigger a new version number. 

The SHACL published by BIG to the web will reflect the most current official version. Users of BIG outputs are encouraged to create their own branch of this repository and accept later official versions when ready to implement these changes. Alternatively, for each tagged version of the repository (e.g. https://github.com/bf-interop/DCTap/tags), one can download the zip or tar files with the version embedded in the folder name.

Versioning support for BIG DCTAP and SHACL may evolve as use cases emerge.

## DCTAP Files
* [Monograph DCTAP](https://github.com/bf-interop/DCTap/tree/main/Monograph%20DCTAP)
* [Serial DCTAP](https://github.com/bf-interop/DCTap/tree/main/Serials%20DCTAP)

