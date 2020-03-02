""" This script holds the function for plotting the groundtracks. """

from astropy import units as u
from astropy import coordinates as coord
from poliastro.examples import iss
import numpy as np
import plotly.graph_objects as go


def groundtrack(orbit,tof= None,label='Satellite Groundtrack',color= 'blue',width=2,title='Groundtrack plot of the satellite',showland = True,showcountries = False,showocean = True,landcolor = 'rgb(229, 236, 246)',oceancolor = 'rgb(255, 255, 255)',projection='equirectangular',lat_grid = False,lat_width = 0.5,lon_grid=False,lon_width=0.5):
        """ Plots the groundtrack of an Orbit.
        Parameters
        ----------
        orbit: poliastro.twobody.orbit.Orbit
        Orbit for making the groundtrack

        tof: float
        Time of flight in hrs

        label: string
        Label of the plot
        
        color: string of the color/rgb
        Color of the plot

        width: int
        Width of the line of the plot

        title: string
        Title of the map

        showland: True/False
        Whether to show the land or not

        showcountries: True/False
        Whether to show the countries or not

        showocean: True/False
        Whether to show the ocean or not

        landcolor: string of the color/rgb
        Color of the land

        oceancolor:  string of the color/rgb
        Color of the ocean

        projection: 'equirectangular', 'mercator', 'orthographic', 'natural earth', 'kavrayskiy7', 'miller', 'robinson', 'eckert4', 'azimuthal equal area', 'azimuthal equidistant', 'conic equal area', 'conic conformal', 'conic equidistant', 'gnomonic', 'stereographic', 'mollweide', 'hammer', 'transverse mercator', 'albers usa', 'winkel tripel', 'aitoff' and 'sinusoidal'.
        Projection type of the map

        lat_grid: True/False
        To show grid lines of the latitude or not

        lat_width: int
        Specify the width of the lat_grid

        lon_grid: True/False
        To show grid lines of the longitude or not

        lon_width: int
        Specify the width of the lon_grid
        ----------
    
        """
        # Calculation of orbital period in rad
        orbit_period=orbit.period.to(u.h).value
        orbit_period_rad=orbit.nu.to(u.rad).value+2*np.pi

        # Calculation of time_span
        if tof is not None:
                time_span=(tof*orbit_period_rad)/orbit_period
        else:
                time_span=orbit_period_rad

        # Transforming GCRS to ITRS        
        orbit_gcrs=orbit.sample(max_anomaly=time_span*u.rad)
        orbit_itrs=orbit_gcrs.transform_to(coord.ITRS(obstime=orbit_gcrs.obstime))
        
        # Converting into lat and lon 
        latlon = orbit_itrs.represent_as(coord.SphericalRepresentation)

        # Plotting the groundtrack
        fig = go.Figure()
        fig.add_trace(go.Scattergeo(
                lat = latlon.lat.to(u.deg),
                lon = latlon.lon.to(u.deg),
                mode = 'lines',
                name= label,
                showlegend= True ,
                line = dict(width = width, color = color,
                )))
        
        fig.update_layout(
                title_text = title,
                
                geo = dict(
                        showland = showland,
                        showcountries = showcountries,
                        showocean = showocean,
                        
                        landcolor = landcolor,
                        
                        oceancolor = oceancolor,
                        projection = dict(
                                type = projection,
                                ),
                lonaxis = dict(
                        showgrid = lat_grid,
                        
                        gridwidth = lat_width
                        ),
                lataxis = dict(
                        showgrid = lon_grid,
                        
                        gridwidth = lon_width
                        )
                )   
        )

        fig.show()

    

