for i in 0.3
do
  # CUDA_VISIBLE_DEVICES=0 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/opv2v_pose_error/opv2v_hybrie_late_test --fusion_method late --pose_err $i  --note late_pose_err_$i &
  # CUDA_VISIBLE_DEVICES=1 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/opv2v_pose_error/opv2v_point_pillar_lidar_early_2023_01_14_23_39_47 --fusion_method early --pose_err $i  --note early_pose_err_$i &
  # CUDA_VISIBLE_DEVICES=2 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/opv2v_pose_error/opv2v_point_pillar_lidar_fcooper_2023_01_14_23_42_00 --fusion_method intermediate --pose_err $i  --note fcooper_pose_err_$i &
  CUDA_VISIBLE_DEVICES=3 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/opv2v_pose_error/opv2v_point_pillar_lidar_v2vnet_2023_01_14_23_46_48 --fusion_method intermediate --pose_err $i  --note v2vnet_pose_err_$i &
  # CUDA_VISIBLE_DEVICES=6 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/opv2v_pose_error/opv2v_point_pillar_lidar_v2xvit_2023_01_18_09_52_30 --fusion_method intermediate --pose_err $i  --note v2xvit_pose_err_$i &
  # CUDA_VISIBLE_DEVICES=3 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/opv2v_pose_error/opv2v_point_pillar_lidar_disconet_2023_01_17_11_13_31 --fusion_method intermediate --pose_err $i  --note disconet_pose_err_$i &
  CUDA_VISIBLE_DEVICES=3 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/opv2v_point_pillar_lidar_where2comm_2023_01_18_10_45_02 --fusion_method intermediate --pose_err $i  --note where2comm_pose_err_$i &


done