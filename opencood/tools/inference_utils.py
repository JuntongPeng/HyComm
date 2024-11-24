# -*- coding: utf-8 -*-
# Author: Runsheng Xu <rxx3386@ucla.edu>
# License: TDG-Attribution-NonCommercial-NoDistrib


import os
from collections import OrderedDict

import numpy as np
import torch

from opencood.utils.common_utils import torch_tensor_to_numpy
from opencood.utils.transformation_utils import get_relative_transformation
from opencood.utils.box_utils import create_bbx, project_box3d, nms_rotated
from opencood.utils.camera_utils import indices_to_depth
from opencood.utils.hybrid_utils import *
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

def inference_late_fusion(batch_data, model, dataset):
    """
    Model inference for late fusion.

    Parameters
    ----------
    batch_data : dict
    model : opencood.object
    dataset : opencood.LateFusionDataset

    Returns
    -------
    pred_box_tensor : torch.Tensor
        The tensor of prediction bounding box after NMS.
    gt_box_tensor : torch.Tensor
        The tensor of gt bounding box.
    """
    # output_dict = OrderedDict()

    # for cav_id, cav_content in batch_data.items():
    #     output_dict[cav_id] = model(cav_content)
    #     pred_box_tensor, pred_score, gt_box_tensor,unc_x,unc_y = \
    #     dataset.post_process(batch_data,
    #                          output_dict)


    # return_dict = {"pred_box_tensor" : pred_box_tensor, \
    #                 "pred_score" : pred_score, \
    #                 "gt_box_tensor" : gt_box_tensor}
        
    output_dict = OrderedDict()
    for cav_id, cav_content in batch_data.items():
        # if(cav_id=='ego'):
        #     continue
        output_dict[cav_id] = model(cav_content)
    # print(output_dict['ego'])
    
    points_num=0
    pred_box_tensor, pred_score, gt_box_tensor,unc_x,unc_y,points_num = \
    dataset.post_process(batch_data,
                             output_dict)


    return_dict = {"pred_box_tensor" : pred_box_tensor, \
                    "pred_score" : pred_score, \
                    "gt_box_tensor" : gt_box_tensor,\
                    "unc_x":unc_x,\
                    "unc_y":unc_y,\
                    "points_num":points_num    }
        
    # result_dict = OrderedDict()
    # for cav_id, cav_content in batch_data.items():
    #     output_dict = OrderedDict()
    #     output_dict[cav_id] = model(cav_content)
    #     pred_box_tensor, pred_score, gt_box_tensor,unc_x,unc_y = \
    #         dataset.post_process(batch_data,
    #                             output_dict)
    #     cav_dict={
    #         "pred_box_tensor" : pred_box_tensor, \
    #         "pred_score" : pred_score, \
    #         "gt_box_tensor" : gt_box_tensor,\
    #         "unc_x":unc_x,\
    #         "unc_y":unc_y
    #     }
    #     result_dict[cav_id]=cav_dict
    # return_dict = result_dict

    return return_dict

def inference_hybrid_fusion(batch_data, model, dataset,sampling_rate=1.0):
    """
    Model inference for late fusion.

    Parameters
    ----------
    batch_data : dict
    model : opencood.object
    dataset : opencood.LateFusionDataset

    Returns
    -------
    pred_box_tensor : torch.Tensor
        The tensor of prediction bounding box after NMS.
    gt_box_tensor : torch.Tensor
        The tensor of gt bounding box.
    """
    points_num=0
    # calculate seprately
    #print(batch_data.keys())
    pred_list=[]
    score_list=[]
    #non ego processing:
    non_ego_output_dict = OrderedDict()
    non_ego_data = OrderedDict()
    projected_lidar_stack = []
    object_stack = []
    object_id_stack = []
    pred_box_tensor=[]
    pred_score=[]
    unc=[]

    for cav_id, cav_content in batch_data.items():
        if cav_id=='ego':
            continue
        else :
            non_ego_output_dict[cav_id] = model(cav_content)
            non_ego_data[cav_id] = cav_content
            non_ego_origin_data=cav_content['origin_lidar'][0]
            ne_pred_box_tensor, ne_pred_score, gt_box_tensor,ne_uncx,ne_uncy = \
                dataset.post_process(non_ego_data,
                                    non_ego_output_dict)
            if ne_pred_box_tensor!=None:
                #pred_box_tensor.append(ne_pred_box_tensor)
                #pred_score.append(ne_pred_score)
                #unc.append(ne_uncx**2+ne_uncy**2)
                ne_unc=torch.stack([ne_uncx,ne_uncy])
                non_ego_processed_data,points_num=unc_filtering(non_ego_origin_data,ne_pred_box_tensor,ne_unc,sampling_rate)
                projected_lidar_stack.append(non_ego_processed_data)
                
                points_num=points_num+ne_pred_box_tensor.shape[0]*8
            else:
                points_num=0
    
    
    # non-ego perception done here
    ego_data=OrderedDict()
    ego_output_dict=OrderedDict()

    ego_data['ego']=batch_data['ego']
    projected_lidar_stack.append(ego_data['ego']['origin_lidar'][0].cpu())
    
    # fused early point clouds
    projected_lidar_stack = np.vstack(projected_lidar_stack)
    
    processed_lidar=dataset.pre_processor.preprocess(projected_lidar_stack)
    
    processed_lidar = dataset.pre_processor.collate_batch(
                        [processed_lidar])
    
    processed_lidar['voxel_features']=processed_lidar['voxel_features'].cuda()
    processed_lidar['voxel_num_points']=processed_lidar['voxel_num_points'].cuda()
    processed_lidar['voxel_coords']=processed_lidar['voxel_coords'].cuda()
    ego_data['ego']['processed_lidar']=processed_lidar

    batch_data['ego']['origin_lidar']=torch.tensor(projected_lidar_stack)
    
    ego_output_dict['ego']=model(ego_data['ego'])
    e_pred_box_tensor, e_pred_score, gt_box_tensor,e_uncx,e_uncy = \
                dataset.post_process(ego_data,
                                    ego_output_dict)
    
    pred_box_tensor.append(e_pred_box_tensor)
    pred_score.append(e_pred_score)
    unc.append(e_uncx**2+e_uncy**2)

    pred_box_tensor=torch.cat(pred_box_tensor)
    pred_score=torch.cat(pred_score)
    unc_score=torch.cat(unc)
    # unc_score=-100*unc_score
    # keep_index=nms_rotated(pred_box_tensor,
    #                                        unc_score,
    #                                        0.15
    #                                        )
    # pred_box_tensor=pred_box_tensor[keep_index]
    # pred_score=pred_score[keep_index]
    # unc_score=unc_score[keep_index]
    assert pred_box_tensor.shape[0]==pred_score.shape[0]
    
    print(points_num)
    return_dict = {"pred_box_tensor" :pred_box_tensor, \
                    "pred_score" : pred_score, \
                    "gt_box_tensor" : gt_box_tensor,\
                    "late_point_num": points_num,\
                    "unc_score":unc_score}
    return return_dict


def inference_no_fusion(batch_data, model, dataset, single_gt=False):
    """
    Model inference for no fusion.

    Parameters
    ----------
    batch_data : dict
    model : opencood.object
    dataset : opencood.LateFusionDataset

    Returns
    -------
    pred_box_tensor : torch.Tensor
        The tensor of prediction bounding box after NMS.
    gt_box_tensor : torch.Tensor
        The tensor of gt bounding box.
    single_gt : bool
        if True, only use ego agent's label.
        else, use all agent's merged labels.
    """
    output_dict_ego = OrderedDict()
    if single_gt:
        batch_data = {'ego': batch_data['ego']}
        
    output_dict_ego['ego'] = model(batch_data['ego'])
    # output_dict only contains ego
    # but batch_data havs all cavs, because we need the gt box inside.

    pred_box_tensor, pred_score, gt_box_tensor = \
        dataset.post_process_no_fusion(batch_data,  # only for late fusion dataset
                             output_dict_ego)

    return_dict = {"pred_box_tensor" : pred_box_tensor, \
                    "pred_score" : pred_score, \
                    "gt_box_tensor" : gt_box_tensor}
    return return_dict

def inference_no_fusion_w_uncertainty(batch_data, model, dataset):
    """
    Model inference for no fusion.

    Parameters
    ----------
    batch_data : dict
    model : opencood.object
    dataset : opencood.LateFusionDataset

    Returns
    -------
    pred_box_tensor : torch.Tensor
        The tensor of prediction bounding box after NMS.
    gt_box_tensor : torch.Tensor
        The tensor of gt bounding box.
    """
    output_dict_ego = OrderedDict()

    output_dict_ego['ego'] = model(batch_data['ego'])
    # output_dict only contains ego
    # but batch_data havs all cavs, because we need the gt box inside.

    pred_box_tensor, pred_score, gt_box_tensor, uncertainty_tensor = \
        dataset.post_process_no_fusion_uncertainty(batch_data, # only for late fusion dataset
                             output_dict_ego)

    return_dict = {"pred_box_tensor" : pred_box_tensor, \
                    "pred_score" : pred_score, \
                    "gt_box_tensor" : gt_box_tensor, \
                    "uncertainty_tensor" : uncertainty_tensor}

    return return_dict


def inference_early_fusion(batch_data, model, dataset):
    """
    Model inference for early fusion.

    Parameters
    ----------
    batch_data : dict
    model : opencood.object
    dataset : opencood.EarlyFusionDataset

    Returns
    -------
    pred_box_tensor : torch.Tensor
        The tensor of prediction bounding box after NMS.
    gt_box_tensor : torch.Tensor
        The tensor of gt bounding box.
    """
    output_dict = OrderedDict()
    #print(batch_data.keys())
    cav_content = batch_data['ego']
    output_dict['ego'] = model(cav_content)
    

    # should read params
    if True :
        pred_box_tensor, pred_score, gt_box_tensor,unc_x,unc_y,diff_x,diff_y = \
            dataset.post_process(batch_data,
                             output_dict)
        #print("unc_x",unc_x.shape)
        return_dict = { "pred_box_tensor" : pred_box_tensor, \
                        "pred_score" : pred_score, \
                        "gt_box_tensor" : gt_box_tensor,\
                        "unc_x":unc_x,\
                        "unc_y":unc_y,\
                        "diff_x":diff_x,\
                        "diff_y":diff_y}
    else:
        pred_box_tensor, pred_score, gt_box_tensor = \
            dataset.post_process(batch_data,
                             output_dict)
        return_dict = {"pred_box_tensor" : pred_box_tensor, \
                    "pred_score" : pred_score, \
                    "gt_box_tensor" : gt_box_tensor}

    

    if "depth_items" in output_dict['ego']:
        return_dict.update({"depth_items" : output_dict['ego']['depth_items']})
    return return_dict


def inference_intermediate_fusion(batch_data, model, dataset):
    """
    Model inference for early fusion.

    Parameters
    ----------
    batch_data : dict
    model : opencood.object
    dataset : opencood.EarlyFusionDataset

    Returns
    -------
    pred_box_tensor : torch.Tensor
        The tensor of prediction bounding box after NMS.
    gt_box_tensor : torch.Tensor
        The tensor of gt bounding box.
    """
    return_dict = inference_early_fusion(batch_data, model, dataset)
    return return_dict

def inference_intermediate_fusion_withcomm(batch_data, model, dataset):
    """
    Model inference for early fusion.

    Parameters
    ----------
    batch_data : dict
    model : opencood.object
    dataset : opencood.EarlyFusionDataset

    Returns
    -------
    pred_box_tensor : torch.Tensor
        The tensor of prediction bounding box after NMS.
    gt_box_tensor : torch.Tensor
        The tensor of gt bounding box.
    """
    output_dict = OrderedDict()
    cav_content = batch_data['ego']
    output_dict['ego'] = model(cav_content)
    
    pred_box_tensor, pred_score, gt_box_tensor = \
        dataset.post_process(batch_data,
                             output_dict)
    comm_rates = output_dict['ego']['comm_rate']
    return_dict = {"pred_box_tensor" : pred_box_tensor, \
                    "pred_score" : pred_score, \
                    "gt_box_tensor" : gt_box_tensor,\
                    "comm_rates":comm_rates}
    
    return return_dict

def save_prediction_gt(pred_tensor, gt_tensor, pcd, timestamp, save_path):
    """
    Save prediction and gt tensor to txt file.
    """
    pred_np = torch_tensor_to_numpy(pred_tensor)
    gt_np = torch_tensor_to_numpy(gt_tensor)
    pcd_np = torch_tensor_to_numpy(pcd)

    np.save(os.path.join(save_path, '%04d_pcd.npy' % timestamp), pcd_np)
    np.save(os.path.join(save_path, '%04d_pred.npy' % timestamp), pred_np)
    np.save(os.path.join(save_path, '%04d_gt.npy' % timestamp), gt_np)


def depth_metric(depth_items, grid_conf):
    # depth logdit: [N, D, H, W]
    # depth gt indices: [N, H, W]
    depth_logit, depth_gt_indices = depth_items
    depth_pred_indices = torch.argmax(depth_logit, 1)
    depth_pred = indices_to_depth(depth_pred_indices, *grid_conf['ddiscr'], mode=grid_conf['mode']).flatten()
    depth_gt = indices_to_depth(depth_gt_indices, *grid_conf['ddiscr'], mode=grid_conf['mode']).flatten()
    rmse = mean_squared_error(depth_gt.cpu(), depth_pred.cpu(), squared=False)
    return rmse


def fix_cavs_box(pred_box_tensor, gt_box_tensor, pred_score, batch_data):
    """
    Fix the missing pred_box and gt_box for ego and cav(s).
    Args:
        pred_box_tensor : tensor
            shape (N1, 8, 3), may or may not include ego agent prediction, but it should include
        gt_box_tensor : tensor
            shape (N2, 8, 3), not include ego agent in camera cases, but it should include
        batch_data : dict
            batch_data['lidar_pose'] and batch_data['record_len'] for putting ego's pred box and gt box
    Returns:
        pred_box_tensor : tensor
            shape (N1+?, 8, 3)
        gt_box_tensor : tensor
            shape (N2+1, 8, 3)
    """
    if pred_box_tensor is None or gt_box_tensor is None:
        return pred_box_tensor, gt_box_tensor, pred_score, 0
    # prepare cav's boxes

    # if key only contains "ego", like intermediate fusion
    if 'record_len' in batch_data['ego']:
        lidar_pose =  batch_data['ego']['lidar_pose'].cpu().numpy()
        N = batch_data['ego']['record_len']
        relative_t = get_relative_transformation(lidar_pose) # [N, 4, 4], cav_to_ego, T_ego_cav
    # elif key contains "ego", "641", "649" ..., like late fusion
    else:
        relative_t = []
        for cavid, cav_data in batch_data.items():
            relative_t.append(cav_data['transformation_matrix'])
        N = len(relative_t)
        relative_t = torch.stack(relative_t, dim=0).cpu().numpy()
        
    extent = [2.45, 1.06, 0.75]
    ego_box = create_bbx(extent).reshape(1, 8, 3) # [8, 3]
    ego_box[..., 2] -= 1.2 # hard coded now

    box_list = [ego_box]
    
    for i in range(1, N):
        box_list.append(project_box3d(ego_box, relative_t[i]))
    cav_box_tensor = torch.tensor(np.concatenate(box_list, axis=0), device=pred_box_tensor.device)
    
    pred_box_tensor_ = torch.cat((cav_box_tensor, pred_box_tensor), dim=0)
    gt_box_tensor_ = torch.cat((cav_box_tensor, gt_box_tensor), dim=0)

    pred_score_ = torch.cat((torch.ones(N, device=pred_score.device), pred_score))

    gt_score_ = torch.ones(gt_box_tensor_.shape[0], device=pred_box_tensor.device)
    gt_score_[N:] = 0.5

    keep_index = nms_rotated(pred_box_tensor_,
                            pred_score_,
                            0.01)
    pred_box_tensor = pred_box_tensor_[keep_index]
    pred_score = pred_score_[keep_index]

    keep_index = nms_rotated(gt_box_tensor_,
                            gt_score_,
                            0.01)
    gt_box_tensor = gt_box_tensor_[keep_index]

    return pred_box_tensor, gt_box_tensor, pred_score, N


def get_cav_box(batch_data):
    """
    Args:
        batch_data : dict
            batch_data['lidar_pose'] and batch_data['record_len'] for putting ego's pred box and gt box
    """

    # if key only contains "ego", like intermediate fusion
    if 'record_len' in batch_data['ego']:
        lidar_pose =  batch_data['ego']['lidar_pose'].cpu().numpy()
        N = batch_data['ego']['record_len']
        relative_t = get_relative_transformation(lidar_pose) # [N, 4, 4], cav_to_ego, T_ego_cav
        lidar_agent_record = batch_data['ego']['lidar_agent_record'].cpu().numpy()

    # elif key contains "ego", "641", "649" ..., like late fusion
    else:
        relative_t = []
        lidar_agent_record = []
        for cavid, cav_data in batch_data.items():
            relative_t.append(cav_data['transformation_matrix'])
            lidar_agent_record.append(1 if 'processed_lidar' in cav_data else 0)
        N = len(relative_t)
        relative_t = torch.stack(relative_t, dim=0).cpu().numpy()

        

    extent = [0.2, 0.2, 0.2]
    ego_box = create_bbx(extent).reshape(1, 8, 3) # [8, 3]
    ego_box[..., 2] -= 1.2 # hard coded now

    box_list = [ego_box]
    
    for i in range(1, N):
        box_list.append(project_box3d(ego_box, relative_t[i]))
    cav_box_np = np.concatenate(box_list, axis=0)


    return cav_box_np, lidar_agent_record