import math


def rpm_to_rads(rpm):
    """Convert RPM to rads-1"""
    return (rpm * 2 * math.pi) / 60
