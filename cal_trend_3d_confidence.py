#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Debangshu Banerjee
"""

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def calculate_trend_3d_confidence(data, time_dim=-1, confidence=95):
    """
    ---------------------------------------------------------------------------------------------
    Calculate the linear trend (slope) over time for a 3D dataset and return trends
    significant at the given confidence level.
    
    Parameters:
    -----------
    data (numpy array): A 3D numpy array representing data over time.
    time_dim (int): The index of the time dimension in the data (default is -1, last dimension).
    confidence (float): The confidence level (e.g., 95 for 95% confidence, 99 for 99% confidence).
    
    Returns:
    ------- 
    trend (numpy array): A 2D numpy array (lat, lon) representing the significant slope (trend)
                         for each grid point. Non-significant trends are set to NaN.
    ---------------------------------------------------------------------------------------------
    """
    # Move the time dimension to the last axis if it's not already
    if time_dim != -1:
        data = np.moveaxis(data, time_dim, -1)
    
    # Get the new dimensions of the data
    lat, lon, time = data.shape

    # Convert confidence level to p-value threshold
    p_value_threshold = 1 - confidence / 100.0

    # Create an array of time points (e.g., time indices)
    time_points = np.arange(time)

    # Initialize an array to hold the trend values (slopes) for each lat-lon point
    trend = np.full((lat, lon), np.nan)  # Initialize with NaNs (for non-significant trends)

    # Calculate the trend (slope) for each (lat, lon) point
    for i in range(lat):
        for j in range(lon):
            # Extract the time series for this (lat, lon) point
            y = data[i, j, :]
            
            # Perform linear regression
            slope, intercept, r_value, p_value, std_err = stats.linregress(time_points, y)
            
            # Check if the trend is significant based on the specified confidence level
            if p_value < p_value_threshold:
                trend[i, j] = slope  # Only store the slope if it is significant

    return trend
