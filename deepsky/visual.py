import numpy as np
import matplotlib.pyplot as plt
import xarray as xr


def plot_generated_patch_layer(patch_file, patch_layer, num_plot_rows, num_plot_cols, fig_path,
                               figsize=(12, 12), vmin=0, vmax=80, step=5, cmap="YlOrRd",
                               title_start="GAN Patches", colorbar_label="Data",
                               title_fontsize=16, colorbar_fontsize=14, dpi=300):
    """
    Plot a single layer/channel from a set of patches generated by a GAN
    
    Args:
        patch_file: netCDF file containing generated patches
        patch_layer: which layer to plot
        num_plot_rows: number of subplot rows
        num_plot_cols: number of subplot columns
        fig_path: Path to figure output
        figsize (tuple): Width and height of figure in inches
        vmin: Minimum plotted contour value
        vmax: Maximum plotted contour value
        step: spacing between contours
        cmap: color map
        title_start: Beginning of figure title
        colorbar_label: Label for colorbar (should be long name for quantity being plotted)
        title_fontsize: Font size of the title
        colorbar_fontsize: Font size of the colorbar label and ticks
        dpi: dots per inch

    Returns:

    """
    patches = xr.open_dataset(patch_file)
    patch_file_comps = patch_file.split("/")[-1][:-3].split("_")
    config = int(patch_file_comps[3])
    epoch = int(patch_file_comps[5])
    fig, axes = plt.subplots(num_plot_rows, num_plot_cols, figsize=figsize)
    plt.subplots_adjust(0.01, 0.01, 0.95, 0.95, hspace=0, wspace=0)
    cax = fig.add_axes([0.96, 0.02, 0.03, 0.9])
    axef = axes.ravel()
    contours = np.arange(vmin, vmax + step, step)
    cont = None
    for a, ax in enumerate(axef):
        cont = ax.contourf(patches["gen_patch"][a, :, :, patch_layer], contours, cmap=cmap)
        ax.axes.get_xaxis().set_ticks([])
        ax.axes.get_yaxis().set_ticks([])
        ax.set_xlim(0, 64)
        ax.set_ylim(0, 64)
    cbar = fig.colorbar(cont, cax=cax)
    cbar.ax.tick_params(labelsize=colorbar_fontsize)
    cbar.ax.set_ylabel(colorbar_label, fontsize=colorbar_fontsize)
    fig.suptitle(title_start + " Config {0:d} Epoch {1:d}".format(config, epoch),
                 fontsize=title_fontsize, fontweight="bold", y=0.97)
    plt.savefig(fig_path + "patch_config_{0:03d}_epoch_{1:02d}_images_{2:03d}.png".format(config,
                                                                                          epoch,
                                                                                           axef.size),
                dpi=dpi, bbox_inches="tight")
    plt.close()
    patches.close()
