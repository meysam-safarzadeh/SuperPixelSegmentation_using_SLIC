#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 17:30:57 2023

@author: Meysam
"""


import matplotlib.pyplot as plt
import numpy as np
from skimage.color import rgb2lab, label2rgb
from skimage.segmentation import slic, mark_boundaries, slic_superpixels
from skimage import io

from skimage.measure import regionprops
from skimage.future.graph import rag_mean_color, show_rag, cut_threshold, merge_hierarchical

from skimage.filters import gaussian
from skimage import segmentation, color, filters
from skimage.future import graph


def display_inital_segmentaion(adabtive_SLIC, label, image, im_number, n_segments, compactness='adabtive'):
  """ SHOWING SLIC/Adabtive SLIC segmentation results
  SLIC_type is string "SLIC" or "adabtive SLIC"""
  if adabtive_SLIC:
    SLIC_type = 'Adabtive SLIC'
  else:
    SLIC_type = 'SLIC'
  label = label.astype(int)
  label_rgb = label2rgb(label, image=image, kind='avg')
  label_rgb = np.interp(label_rgb, (label_rgb.min(), label_rgb.max()), (0, 1))
  plt.figure(dpi=200)
  plt.imshow(label_rgb)
  plt.title(SLIC_type + ' segmentation - picture ' + str(im_number) + 
            '\n compactness: ' + str(compactness) + 
            '     number of segments: ' + str(n_segments))

  label_rgb = mark_boundaries(image=image, label_img=label, color=(0, 0, 0))
  plt.figure(dpi=200)
  plt.imshow(label_rgb)
  plt.title(SLIC_type + ' segmentation on original image - picture ' + str(im_number) + 
            '\n compactness: ' + str(compactness) + 
            '     number of segments: ' + str(n_segments))

def Ncuts_merging(adabtive_SLIC, label, image, im_number, thresh, n_segments, num_cuts, compactness='Adabtive'):
  """Ncuts on the RAG"""
  if adabtive_SLIC:
    SLIC_type = 'Adabtive SLIC'
  else:
    SLIC_type = 'SLIC'
  rag = rag_mean_color(image, label, mode='similarity')
  Ncuts_label = graph.cut_normalized(label, rag, thresh=thresh, num_cuts=num_cuts)
  new_final_label_rgb = color.label2rgb(Ncuts_label, image, kind='avg', bg_label=0)
  # normalize the output of label2rgb to [0, 1]
  new_final_label_rgb = np.interp(new_final_label_rgb, (new_final_label_rgb.min(), new_final_label_rgb.max()), (0, 1)) 

  plt.figure(dpi=200)
  plt.imshow(new_final_label_rgb)
  plt.title(SLIC_type + ' Segmentation merged by NCuts - picture ' + str(im_number) +
            '\n compactness: ' + str(compactness) + 
            '     number of segments: ' + str(n_segments) +
            '\n Threshold: ' + str(thresh) + 
            '     number of cuts: ' + str(num_cuts))

  label_rgb = mark_boundaries(image=image, label_img=Ncuts_label, color=(0, 0, 0))
  plt.figure(dpi=200)
  plt.imshow(label_rgb)
  plt.title(SLIC_type + ' segmentation on original image merged by Ncuts - picture ' + str(im_number) +
            '\n compactness: ' + str(compactness) + 
            '     number of segments: ' + str(n_segments) +
            '\n Threshold: ' + str(thresh) + 
            '     number of cuts: ' + str(num_cuts))
  return Ncuts_label

def _weight_mean_color(graph, src, dst, n):
    """Callback to handle merging nodes by recomputing mean color.

    The method expects that the mean color of `dst` is already computed.

    Parameters
    ----------
    graph : RAG
        The graph under consideration.
    src, dst : int
        The vertices in `graph` to be merged.
    n : int
        A neighbor of `src` or `dst` or both.

    Returns
    -------
    data : dict
        A dictionary with the `"weight"` attribute set as the absolute
        difference of the mean color between node `dst` and `n`.
    """

    diff = graph.nodes[dst]['mean color'] - graph.nodes[n]['mean color']
    diff = np.linalg.norm(diff)
    return {'weight': diff}


def merge_mean_color(graph, src, dst):
    """Callback called before merging two nodes of a mean color distance graph.

    This method computes the mean color of `dst`.

    Parameters
    ----------
    graph : RAG
        The graph under consideration.
    src, dst : int
        The vertices in `graph` to be merged.
    """
    graph.nodes[dst]['total color'] += graph.nodes[src]['total color']
    graph.nodes[dst]['pixel count'] += graph.nodes[src]['pixel count']
    graph.nodes[dst]['mean color'] = (graph.nodes[dst]['total color'] /
                                     graph.nodes[dst]['pixel count'])

def display_inital_RAG(adabtive_SLIC, label, image, im_number, n_segments, compactness='Adabtive'):
  """ Displaying the graphs and the weights of each graph"""
  if adabtive_SLIC:
    SLIC_type = 'Adabtive SLIC'
  else:
    SLIC_type = 'SLIC'
  
  ## RAG
  rag = rag_mean_color(image, label)

  ## plot
  fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(6, 8))
  lc = show_rag(label, rag, image, img_cmap='gray', ax=ax)
  

  # specify the fraction of the plot area that will be used to draw the colorbar
  fig.colorbar(lc, fraction=0.03, ax=ax)
  fig.dpi = 200
  ax.axis('off')
  plt.title(SLIC_type + ' initial RAG with weight colorbar - picture ' + str(im_number) + 
            '\n compactness: ' + str(compactness) + 
            '     number of segments: ' + str(n_segments))
  plt.tight_layout()
  plt.show()

def Hierarchical_merging(adabtive_SLIC, label, image, im_number, threshold, n_segments, compactness='adabtive'):
  """ Hierarchical merging of the RAG
  # n_segments and compactness are just for plot's title"""
  if adabtive_SLIC:
    SLIC_type = 'Adabtive SLIC'
  else:
    SLIC_type = 'SLIC'
  #RAG
  rag = rag_mean_color(image, label)
  
  Hierarchical_label = merge_hierarchical(labels=label,
                    rag=rag, 
                    thresh=threshold, 
                    in_place_merge=True, 
                    rag_copy=False,
                    merge_func=merge_mean_color,
                    weight_func=_weight_mean_color)

  # Disply the results

  plt.figure(dpi=200)
  fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(6, 8))
  lc = show_rag(label, rag, image, ax=ax)
  fig.colorbar(lc, fraction=0.03, ax=ax)
  fig.dpi = 200
  plt.title(SLIC_type + ' RAG after hierarchical merging - picture ' + str(im_number) +
            '\n compactness: ' + str(compactness) + 
            '     number of segments: ' + str(n_segments) +
            '\n Threshold: ' + str(threshold))

  new_final_label_rgb = label2rgb(Hierarchical_label, image, kind='avg')
  new_final_label_rgb = np.interp(new_final_label_rgb, (new_final_label_rgb.min(), new_final_label_rgb.max()), (0, 1))
  plt.figure(dpi=200)
  plt.imshow(new_final_label_rgb)
  plt.title(SLIC_type + ' Segmentation after hierarchical merging - picture ' + str(im_number) +
            '\n compactness: ' + str(compactness) + 
            '     number of segments: ' + str(n_segments) +
            '\n Threshold: ' + str(threshold))

  Hierarchical_label_rgb = mark_boundaries(image=image, label_img=Hierarchical_label, color=(0, 0, 0))
  plt.figure(dpi=200)
  plt.imshow(Hierarchical_label_rgb)
  plt.title(SLIC_type + ' segmentation after hierarchical merging on original image- picture ' + str(im_number) +
            '\n compactness: ' + str(compactness) + 
            '     number of segments: ' + str(n_segments) +
            '\n Threshold: ' + str(threshold))

from skimage import data, segmentation, filters, color
from skimage.future import graph
from matplotlib import pyplot as plt
def weight_boundary(graph, src, dst, n):
    """
    Handle merging of nodes of a region boundary region adjacency graph.

    This function computes the `"weight"` and the count `"count"`
    attributes of the edge between `n` and the node formed after
    merging `src` and `dst`.


    Parameters
    ----------
    graph : RAG
        The graph under consideration.
    src, dst : int
        The vertices in `graph` to be merged.
    n : int
        A neighbor of `src` or `dst` or both.

    Returns
    -------
    data : dict
        A dictionary with the "weight" and "count" attributes to be
        assigned for the merged node.

    """
    default = {'weight': 0.0, 'count': 0}

    count_src = graph[src].get(n, default)['count']
    count_dst = graph[dst].get(n, default)['count']

    weight_src = graph[src].get(n, default)['weight']
    weight_dst = graph[dst].get(n, default)['weight']

    count = count_src + count_dst
    return {
        'count': count,
        'weight': (count_src * weight_src + count_dst * weight_dst)/count
    }


def merge_boundary(graph, src, dst):
    """Call back called before merging 2 nodes.

    In this case we don't need to do any computation here.
    """
    pass

