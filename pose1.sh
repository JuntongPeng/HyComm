CUDA_VISIBLE_DEVICES=1 python opencood/tools/inference_w_noise.py --model_dir /GPFS/data/yunqiaoyang/opv2v_point_pillar_lidar_where2comm_2023_01_18_10_45_02 &


CUDA_VISIBLE_DEVICES=2 python opencood/tools/inference_w_noise.py --model_dir /GPFS/data/yunqiaoyang/opv2v_pose_error/opv2v_point_pillar_lidar_v2xvit_2023_01_18_09_52_30 &

CUDA_VISIBLE_DEVICES=3 python opencood/tools/inference_w_noise.py --model_dir /GPFS/data/yunqiaoyang/opv2v_pose_error/opv2v_point_pillar_lidar_fcooper_2023_01_14_23_42_00 &

CUDA_VISIBLE_DEVICES=4 python opencood/tools/inference_w_noise.py --model_dir /GPFS/data/yunqiaoyang/opv2v_pose_error/opv2v_point_pillar_lidar_early_2023_01_14_23_39_47 &

CUDA_VISIBLE_DEVICES=5 python opencood/tools/inference_w_noise.py --model_dir /GPFS/data/yunqiaoyang/opv2v_pose_error/opv2v_point_pillar_lidar_disconet_2023_01_17_11_13_31 &
