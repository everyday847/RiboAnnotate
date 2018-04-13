# RiboAnnotate
Annotate RNA secondary structure diagrams with extra information

## Premise

Have you used [RiboDraw](https://github.com/ribokit/RiboDraw) to produce a secondary structure diagram? Wonderful! That must have been a pleasant experience.
There are some features that seemed cumbersome -- or frankly undesirable -- to incorporate into RiboDraw directly.
Chief among these was the ability to annotate secondary structure diagrams with arbitrary metadata.
For example, we have long had [RiboPaint](https://ribokit.github.io/RiboPaint/) for adding colored blocks over an existing secondary structure diagram based on chemical mapping data.
This step naturally may be decoupled from the process of generating the secondary structure diagram itself!
Doing so also reduces the burden on both individual pieces of software, since each can have a simpler and more specialized model of the problem at hand.

## Implementation

RiboAnnotate is a small wrapper around functions provided by [Pillow](https://github.com/python-pillow/Pillow) to manipulate images (input and output management; text placement).
The core idea is that you provide your image file, along with a file describing where each residue is (i.e., the single letter that's displayed).
Your annotations are then positioned based on the position of the residues being annotated, so as to avoid overlaps with other image content.
