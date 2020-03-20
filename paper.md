---
title: "PyEscape: A narrow escape problem simulator package for python"
tags:
  - Python
  - mathematics
  - simulations
  - stochastic
authors:
  - name: Nathan Hughes
    orcid: 0000-0002-4572-5828
    affiliation: 1 # (Multiple affiliations must be quoted)
  - name: Richard J Morris
    affiliation: 1
  - name: Melissa Tomkins
    affiliation: 1
affiliations:
 - name: John Innes Centre, Norwich, UK
   index: 1

date: 24 January 2019
bibliography: paper.bib
---

# Summary

In biology many research questions focus on uncovering the mechanisms which
allow particles (molecules, proteins etc.) to move from one location to another.
Often these movements are from one domain to another and these domains are in
some way contained. The "narrow escape problem" is a bio-physics problem where
the solution would provide the average time required for a Brownian particle to
escape a bounded domain through a particular opening. Originally proposed by
(@holcmanEscapeSmallOpening2004), solutions to this problem have been given and
refined over the years (@schussNarrowEscapeProblem2007).

Recently, solutions have been given @kayeFastSolverNarrow2020 for more complex
narrow escape problems, such as arbitrary escape pore patterning and size
variation. However, these are provided without easily accessible implementations
and confine the problem to a single container shape. 

Here, we present a novel Python library which enables stochastic simulations to
be ran in order to approximate the narrow escape problem for unique scenarios.
The mathematical models provided are implementations of random-walks in
3-dimensions, (@codlingRandomWalkModels2008). With our models we show that they are
good approximations for analytical solutions ([example
notebook](https://github.com/SirSharpest/NarrowEscapeSimulator/blob/master/notebooks/Examples.ipynb)),
and that they can be scaled to many custom problems.


Through this library we provide functionality for both cube and spherical shaped
domains. We enable a broad range of simulation variables to control, in the most
simple case a user will select the volume and shape they wish to act as their
container, the number and size of escape pores on the container's surface and
the diffusion coefficient of the particle of interest.
Additionally, we give an implementation of Fibonacci spheres which allows for
the fast placement of escape pores pseudo-evenly spaced on the surface of a
sphere, this is often useful in experiments to test how number of escapes
relates to mean escape time.


# External libraries used 

The models given are implemented through NumPy
(@vanderwaltNumPyArrayStructure2011), results are visualised through Matplotlib
(@hunterMatplotlib2DGraphics2007a) and documentation has been implemented using
Jupyter-notebooks (@Kluyver:2016aa)) .

# Acknowledgements

We acknowledge the Norwich Research Park Doctoral Training programme (NRDTP),
European Research Council and the Biotechnology and Biological Sciences Research
Council (BBSRC) for their support and funding.

# References
