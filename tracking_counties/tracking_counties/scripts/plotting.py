# ---------------------------------------------------------------------------- #
# IMPORT #
import pathlib as pl
import plotnine as p9
import siuba as s

from ..config import ROOT_DIR
from .mapping import adjust_crs, shift_meridian

# ---------------------------------------------------------------------------- #
# CLASSES / FUNCTIONS #

def generate_plot_data(
        gdf_county, 
        gdf_state, 
        non_contiguous_codes, 
        epsg_code
        ):

    # Init
    dct_plot = {
        'state': {},
        'county': {}
    }

    # CONTIGUOUS US -----------------------------------
    plot_label = 'contiguous'

    # Reduce state and county datasets to only entities
    # within the contiguous United States.
    dct_plot['state'][plot_label] = (
        gdf_state
        >> s.filter(~s._.geoid.isin(non_contiguous_codes)
        )
    )

    dct_plot['county'][plot_label] = (
        gdf_county
        >> s.filter(~s._.statefp.isin(non_contiguous_codes)
        )
    )

    # Adjust the projections of the map geometries. We are only
    # adjusting the contigous us for now. Alaska and Hawaii
    # plot better with the default projection

    dct_plot['state'][plot_label] = \
        adjust_crs(dct_plot['state'][plot_label], epsg = epsg_code)

    dct_plot['county'][plot_label] = \
        adjust_crs(dct_plot['county'][plot_label], epsg = epsg_code)
    
    # ALASKA -----------------------------------
    plot_label = 'alaska'

    dct_plot['state'][plot_label] = (
        gdf_state
        >> s.filter(s._.geoid == '02')
        )   

    dct_plot['county'][plot_label] = (
        gdf_county
        >> s.filter(s._.statefp == '02')
        )
    
    # Adjust centerline of Alaskan projection. The western edge of the 
    # Aluetian islands lie west of the 180 deg meridian. On the deault
    # map projection, this means Alaska is not projected as one 
    # contiguous object. Instead, the far western edge of the
    # Aleutians are plotted on the far right of the plot, while the rest 
    # of Alaska is plotted on the far right. In order to plot Alaska
    # as a single entity, we need to shift where the projection thinks
    # the maps central meridian lies. 

    # Define new center meridian
    cl = 90

    # Shift projections
    dct_plot['state'][plot_label] = shift_meridian(
        dct_plot['state'][plot_label], 
        cl
        )
    dct_plot['county'][plot_label] = shift_meridian(
        dct_plot['county'][plot_label], 
        cl
        )
    
    # HAWAII -----------------------------------
    dct_plot['state'][plot_label] = (
        gdf_state
        >> s.filter(s._.geoid == '15')
        )   

    dct_plot['county'][plot_label] = (
        gdf_county
        >> s.filter(s._.statefp == '15')
        )

    # North Carolina -----------------------------------
    dct_plot['state'][plot_label] = (
        gdf_state
        >> s.filter(s._.geoid == '37')
        )   

    dct_plot['county'][plot_label] = (
        gdf_county
        >> s.filter(s._.statefp == '37')
        )

    # Southeast -----------------------------------
    state_codes = [
        '13', '37', '45', '47', '51'
    ]

    dct_plot['state'][plot_label] = (
        gdf_state
        >> s.filter(s._.geoid.isin(state_codes))
        )   

    dct_plot['county'][plot_label] = (
        gdf_county
        >> s.filter(s._.statefp.isin(state_codes))
        )
    
    return dct_plot


class Plot:
    def __init__(self, plot_tables, plot_params, units = "in", dpi = 1000):
        self.plot_tables = plot_tables
        self.plot_params = plot_params
        self.units = units
        self.dpi = dpi
        self.plot_dir = pl.PurePath(ROOT_DIR, 'data', 'plots')
    

    def __call__(self, plot_label, print_plot = True, save_plot = True):
        p = self.generate_plot(plot_label = plot_label)

        if save_plot:
            self.save_plot(
                plot = p, 
                plot_label = plot_label
                )
            
        if print_plot:
            print(p)


    def generate_plot(self, plot_label):

        p = (
            p9.ggplot() +
            p9.geom_map(
                data = self.plot_tables['county'][plot_label],
                mapping = p9.aes(
                    fill = 'visited'
                ),
                color = self.plot_params['entity_border']['color']['county'],
                size = self.plot_params['entity_border']['thickness']['county'],
                ) +
            p9.geom_map(
                data = self.plot_tables['state'][plot_label],
                mapping = p9.aes(
                    fill = 'visited',
                    alpha = 'visited'
                ),
                color = self.plot_params['entity_border']['color']['state'],
                size = self.plot_params['entity_border']['thickness']['state']
                ) +
            p9.scale_fill_manual(
                values = self.plot_params['color'], 
                guide  = False
                ) + 
            p9.scale_alpha_manual(
                values = self.plot_params['opacity'],
                guide  = False
                ) + 
            p9.theme_linedraw() + 
            p9.theme(
                figure_size = (
                    self.plot_params['dimensions']['width'][plot_label],
                    self.plot_params['dimensions']['height'][plot_label]
                    ),
                    axis_text = p9.element_blank(),
                    axis_ticks = p9.element_blank(),
                    panel_border = p9.element_rect(
                        fill  = "#000000", 
                        color = "#000000", 
                        size  = 2
                        ),
                    panel_grid_major = p9.element_blank(),
                    panel_grid_minor = p9.element_blank(),
            )
        )

        if plot_label == 'hawaii':
            p += p9.coord_cartesian(
                xlim = (-162, -153),
                ylim = (16, 26)
            ) 
    
        return p
    

    def save_plot(self, plot, plot_label):
        plot_path = pl.PurePath(self.plot_dir, f'{plot_label}.png')
        plot.save(
            filename = plot_path,
            height   = self.plot_params['dimensions']['height'][plot_label],
            width    = self.plot_params['dimensions']['width'][plot_label],
            units    = self.units,
            dpi      = self.dpi
        )



