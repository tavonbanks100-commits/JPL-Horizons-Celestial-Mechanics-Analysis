# JPL-Horizons-Celestial-Mechanics-Analysis
Python tool for retrieving and analyzing NASA JPL Horizons ephemeris data, including planetary positions, velocities, distances, and spacecraft trajectories.
JPL Horizons — Celestial Mechanics Analysis

Overview

An independent computational astronomy project developed in Python to explore celestial-body positions, velocities, and orbital motion using NASA JPL Horizons ephemeris data.

The project uses a modular Python architecture, separating core astronomical calculations from the main analysis scripts.

Project Architecture

Main Analysis Script

Provides the primary interface for selecting celestial objects, observation times, and reference centers. Uses the core module to perform astronomical calculations and analyze retrieved data.

horizons_core.py

Contains reusable functionality supporting the main Horizons analysis program.

Separating the core functionality from the main script helps organize the code and makes it easier to expand the project with additional astronomical analyses.

Research Objectives

* Retrieve celestial position and velocity data from JPL Horizons.
* Calculate three-dimensional distances and velocity magnitudes.
* Examine relative motion between celestial objects.
* Explore planetary and spacecraft trajectories.
* Apply computational techniques to celestial mechanics.

Mathematical Foundations

Position vector magnitude:

r = √(x² + y² + z²)

Velocity vector magnitude:

v = √(vx² + vy² + vz²)

These calculations determine distance and speed relative to the selected reference origin and frame.

Technologies

* Python
* Astroquery
* NASA JPL Horizons
* Numerical analysis

Running the Project

Install the required dependencies, then execute the main Horizons Python script.

The main script and horizons_core.py should remain in the same directory unless the imports are configured differently.

Scientific Limitations

Results depend on the selected ephemeris, reference frame, and observation times. Analyzing position and velocity data alone does not establish the gravitational causes of a trajectory.

This is an independent educational research project, not an official NASA or JPL application.

Author

Tavon Banks

Physics Major | Astronomy Minor
Arizona State University

Space Studies — Astronomy
American Military University

Research Interests: Astrophysics, Celestial Mechanics, Computational Astronomy, and Spacecraft Dynamics.
