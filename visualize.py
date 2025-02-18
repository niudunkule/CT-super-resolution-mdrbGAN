"""
This module contains all methods and functions necessary for visualization.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.colors import LinearSegmentedColormap
import wget
from zipfile import ZipFile

class FontsScheme:
    """
    This class defines the fonts used in plotting.

    Attributes:
         title_font: font used for titles
         labels_font: font used for labels
         text_font: font used for text
         textS_font: font used for small text
    """
    def __init__(self, fonts_dir):
        """
        :param fonts_dir: path to the directory that will contain the downloaded font
        """

        # Download and unzip the Avenir font
        if not os.path.exists(fonts_dir):
            os.mkdir(fonts_dir)
        if not os.path.exists(os.path.join(fonts_dir, 'avenir_ff')):
            font_url = "https://github.com/niudunkule/CT-super-resolution-mdrbGAN/raw/master/Avenir-Font.zip"
            font_zip_path = wget.download(font_url, out=fonts_dir)
            with ZipFile(font_zip_path, 'r') as zipObj:
                zipObj.extractall(path=fonts_dir)

        regular_font_path = os.path.join(fonts_dir, "avenir_ff/AvenirLTStd-Book.otf")
        bold_font_path = os.path.join(fonts_dir, "avenir_ff/AvenirLTStd-Black.otf")

        # Define the title font properties
        self.title_font = fm.FontProperties(fname=regular_font_path)
        self.title_font.set_size(16)
        self.title_font.set_style('normal')

        # Define the labels font properties
        self.labels_font = fm.FontProperties(fname=regular_font_path)
        self.labels_font.set_size(14)
        self.labels_font.set_style('normal')

        # Define the texts fonts properties
        self.text_font = fm.FontProperties(fname=regular_font_path)
        self.text_font.set_size(12)
        self.text_font.set_style('normal')
        self.textS_font = fm.FontProperties(fname=regular_font_path)
        self.textS_font.set_size(12)
        self.textS_font.set_style('normal')


class ColorScheme:
    """
    This class contains the colors used in plotting.
    """
    def __init__(self):
        self.coral = '#f56958'
        self.yellow = '#f6e813'
        self.lilac = '#a051a0'
        self.cream = '#fef6e9'
        self.creamT = '#fef6e959'
        self.dark = '#1a1416'
        self.darkT = '#1a1416bf'


class GradientColorMap:
    """
    This class contains the color map used in plotting.

    Attributes:
        colors: list of colors used for the color map
        name: the name of the color map
        num_bins: number of color bins used for creating the color map
    """
    def __init__(self, colors: list):
        """
        :param colors: list of colors used for creating the color map
        """
        self.colors = colors
        self.name = 'gradient_cmap'
        self.num_bins = 100

    def get_cmap(self):
        """
        Method to create color map.
        :return: color map
        """
        cmap = LinearSegmentedColormap.from_list(self.name, self.colors, self.num_bins)
        return cmap


class Visualizer:
    """
    This class containd methods for creating various visualizations for the MER task.
    """
    def __init__(self, fonts_dir, plots_dir):
        """
        :param fonts_dir: path to the directory containing the font
        :param plots_dir: path to the directory the plots will be written to
        """
        self._plots_dir = plots_dir
        self._colors = ColorScheme()
        self._fonts = FontsScheme(fonts_dir)

    def visualize_ct(self, axis, ct_image, title=None, psnr=None):
        """
        Method to create CT image plot.
        :param axis: plot axis
        :param ct_image: CT image to plot
        :param title: plot title
        :param psnr: PSNR score, in the case of super-resolution CT image
        """
        no_spines_plot(axis)
        no_ticks_plot(axis)
        axis.set_aspect('equal')

        img_plot = axis.imshow(ct_image, cmap='gray')

        if title is not None:
            axis.set_ylabel('{:s}\n\n'.format(title.upper()), fontproperties=self._fonts.title_font,
                            color=self._colors.darkT)
        if psnr is not None:
            axis.set_title('PSNR = {:.2f}\n'.format(psnr), fontproperties=self._fonts.labels_font,
                           color=self._colors.darkT)

    def visualize_generated_ct(self, lr_ct, sr_ct, hr_ct, epoch):
        """
        Method to plot triplets of CT images: low-resolution, super-resolution, high-resolution.
        :param lr_ct: low-resolution CT image
        :param sr_ct: super-resolution CT image
        :param hr_ct: high-resolution CT image
        :param epoch: current epoch
        """
        lr_ct, sr_ct, hr_ct = lr_ct.squeeze().numpy(), sr_ct.squeeze().numpy(), hr_ct.squeeze().numpy()

        fig, ax = plt.subplots(3, 8, figsize=(20, 6), gridspec_kw={'hspace': .05, 'wspace': .25})

        for idx in range(8):
            if idx > 0:
                lr_title, sr_title, hr_title = None, None, None
            else:
                lr_title = 'low-res'
                sr_title = 'super-res'
                hr_title = 'high-res'

            # Compute metrics for generated CT image
            hr_range = hr_ct[idx].max() - hr_ct[idx].min()
            mse = ((sr_ct[idx] - hr_ct[idx]) ** 2).mean()
            psnr = 10 * np.log10((hr_range ** 2) / mse)

            self.visualize_ct(ax[0, idx], lr_ct[idx], title=lr_title, psnr=psnr)
            self.visualize_ct(ax[1, idx], sr_ct[idx], title=sr_title)
            self.visualize_ct(ax[2, idx], hr_ct[idx], title=hr_title)

        plt.savefig(os.path.join(self._plots_dir, 'visualization_epoch_{:d}.svg'.format(epoch + 1)))
        plt.close(fig)

    def get_generated_ct_fig(self, lr_ct, sr_ct, hr_ct):
        """
        Method to build figure with triplets of CT images: low-resolution, super-resolution, high-resolution.
        :param lr_ct: low-resolution CT image
        :param sr_ct: super-resolution CT image
        :param hr_ct: high-resolution CT image
        :return: created figure
        """
        lr_ct, sr_ct, hr_ct = lr_ct.squeeze().numpy(), sr_ct.squeeze().numpy(), hr_ct.squeeze().numpy()

        fig, ax = plt.subplots(3, 8, figsize=(20, 6), gridspec_kw={'hspace': .05, 'wspace': .15})

        for idx in range(8):
            if idx > 0:
                lr_title, sr_title, hr_title = None, None, None
            else:
                lr_title = 'low-res'
                sr_title = 'super-res'
                hr_title = 'high-res'

            hr_range = hr_ct[idx].max() - hr_ct[idx].min()
            mse = ((sr_ct[idx] - hr_ct[idx]) ** 2).mean()
            psnr = 10 * np.log10((hr_range ** 2) / mse)

            self.visualize_ct(ax[0, idx], lr_ct[idx], title=lr_title, psnr=psnr)
            self.visualize_ct(ax[1, idx], sr_ct[idx], title=sr_title)
            self.visualize_ct(ax[2, idx], hr_ct[idx], title=hr_title)

        return fig

    def plot_loss(self, axis, train_loss, val_loss):
        """
        Method to plot the train and validation losses.
        :param axis: plot axis
        :param train_loss: loss for training
        :param val_loss: loss for validation
        """
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)
        axis.set_facecolor(self._colors.darkT)

        val_plot = axis.plot(val_loss, color=self._colors.creamT, lw=1)
        train_plot = axis.plot(train_loss, color=self._colors.coral, lw=1)

        xlim = [0, len(train_loss)]
        xticks = np.linspace(xlim[0], xlim[1], 11).astype('int')
        axis.set_xlim(xlim)
        axis.set_xticks(xticks)
        axis.set_xticklabels(['{:d}'.format(tick) for tick in xticks],
                             fontproperties=self._fonts.textS_font, color=self._colors.darkT)

        ylim = axis.get_ylim()
        axis.set_ylim(ylim)
        yticks = np.linspace(ylim[0], ylim[1], num=6, endpoint=True)
        axis.set_yticks(yticks)
        axis.set_yticklabels([str('{:.3f}'.format(tick)) for tick in yticks],
                             fontproperties=self._fonts.textS_font, color=self._colors.darkT)

        axis.tick_params(axis='both', color='black', length=3, width=.75)

        axis.set_title('PERCEPTUAL LOSS\n', fontproperties=self._fonts.labels_font, color=self._colors.darkT)
        legend = axis.legend(['Validation', 'Train'], prop=self._fonts.text_font, framealpha=.25)

    def plot_psnr(self, axis, train_psnr, val_psnr):
        """
        Method to plot the train and validation PSNRs.
        :param axis: plot axis
        :param train_psnr: PSNR for training
        :param val_psnr: PSNR for validation
        """
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)
        axis.set_facecolor(self._colors.darkT)

        val_plot = axis.plot(val_psnr, color=self._colors.creamT, lw=1)
        train_plot = axis.plot(train_psnr, color=self._colors.coral, lw=1)

        xlim = [0, len(train_psnr)]
        xticks = np.linspace(xlim[0], xlim[1], 11).astype('int')
        axis.set_xlim(xlim)
        axis.set_xticks(xticks)
        axis.set_xticklabels(['{:d}'.format(tick) for tick in xticks],
                             fontproperties=self._fonts.textS_font, color=self._colors.darkT)

        ylim = axis.get_ylim()
        axis.set_ylim(ylim)
        yticks = np.linspace(ylim[0], ylim[1], num=6, endpoint=True)
        axis.set_yticks(yticks)
        axis.set_yticklabels([str('{:.2f}'.format(tick)) for tick in yticks],
                             fontproperties=self._fonts.textS_font, color=self._colors.darkT)

        axis.tick_params(axis='both', color='black', length=3, width=.75)

        axis.set_title('PSNR\n', fontproperties=self._fonts.labels_font, color=self._colors.darkT)
        legend = axis.legend(['Validation', 'Train'], prop=self._fonts.text_font, framealpha=.25)

    def visualize_performance(self, train_dict, val_dict, epoch):
        """
        Method to plot losses and PSNR scores for training and validation.
        :param train_dict: dictionary with train information
        :param val_dict: dictionary with validation information
        :param epoch: current training epoch
        """
        fig, ax = plt.subplots(1, 2, figsize=(18, 5), gridspec_kw={'wspace': .25})

        self.plot_loss(ax[0], train_dict['p_loss'], val_dict['p_loss'])
        self.plot_psnr(ax[1], train_dict['psnr'], val_dict['psnr'])

        plt.savefig(os.path.join(self._plots_dir, 'performance_epoch_{:d}.svg'.format(epoch + 1)))
        plt.close(fig)

    def visualize_slice(self, axis, ct_slice, ct_name, scores_dict=None):
        """
        Method to create CT full slice plot.
        :param axis: plot axis
        :param ct_slice: CT slice to plot
        :param ct_name: CT slice name
        :param scores_dict: performance metrics dict, in the case of super-resolution CT image
        """

        no_spines_plot(axis)
        no_ticks_plot(axis)
        axis.set_aspect('equal')

        img_plot = axis.imshow(ct_slice, cmap='gray')

        axis.set_xlabel('\n{:s}'.format(ct_name.upper()), fontproperties=self._fonts.title_font,
                        color=self._colors.darkT)

        if scores_dict is not None:
            title = ' MSE {:.3e}\n'.format(scores_dict['mse'])
            title += 'PSNR {:.3f}\n'.format(scores_dict['psnr'])

            axis.set_title(title, fontproperties=self._fonts.labels_font, color=self._colors.darkT)

    def visualize_full_slices(self, lr_slice, sr_slice, hr_slice, scores_dict, ct_name, epoch):
        """
        Method to visualize triplets of low-resolution, super-resolution and high-resolution CT full slices.
        :param lr_slice: low-resolution CT slice
        :param sr_slice: super-resolution CT slice
        :param hr_slice:high-resolution CT slice
        :param scores_dict: dictionary with performance metrics
        :param ct_name: CT slice name
        :param epoch:current epoch
        """
        fig, ax = plt.subplots(1, 3, figsize=(20, 6), gridspec_kw={'wspace': .15})

        self.visualize_slice(ax[0], lr_slice, 'low-res')
        self.visualize_slice(ax[1], sr_slice, 'super-res', scores_dict)
        self.visualize_slice(ax[2], hr_slice, 'high-res')

        plt.savefig(os.path.join(self._plots_dir, 'test_results_{:s}_{:d}.svg'.format(ct_name, epoch)))
        plt.close(fig)


def no_spines_plot(axis):
    """
    Function to hide spines in plot.
    :param axis: plot axis
    """
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.spines["bottom"].set_visible(False)
    axis.spines["left"].set_visible(False)


def no_ticks_plot(axis):
    """
    Function to hide ticks in plot.
    :param axis: plot axis
    """
    axis.set_xticks([])
    axis.set_yticks([])
