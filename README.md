# 2027 Puppy

Puppy is the outreach FRC robot for team 5113.

## Installation (windows)

Clone the repository:

```powershell
git clone https://github.com/FRC5113/2027-Puppy.git
```

Install in editable mode:

```powershell
pip install -e .
```

Or (alternatively) install requirements.txt:

```powershell
pip install -r requirements.txt
```

## Usage

The robot code is intended to be run on the 2026 version of wpilib, using a RoboRIO and CTRE Phoenix 5 hardware. However, it can be run in simulation regardless of hardware (or lack of it).

### Simulation

Inside of the puppy/ directory, run:

```powershell
robotpy sim
```

This opens up a simulation in the browser, in which you can use an Xbox Controller to drive the robot.

### Deployment to a real robot

Download packages to the RIO:

```powershell
robotpy sync
```

Deploy the code to the RIO:

```powershell
robotpy deploy
```

---
