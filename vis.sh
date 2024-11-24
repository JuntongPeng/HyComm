# CUDA_VISIBLE_DEVICES=3 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/Hybrid_opv2v_vis --box_ratio 0.0 --expansion_ratio 100 --sampling_rate 0.1 --background_ratio 0.1 --sample_method unc --note early_0.1 &

# CUDA_VISIBLE_DEVICES=3 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/Hybrid_opv2v_vis --box_ratio 0.0 --expansion_ratio 100 --sampling_rate 0.01 --background_ratio 0.01 --sample_method unc --note early_0.05 &


# CUDA_VISIBLE_DEVICES=1 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/Hybrid_opv2v_vis --box_ratio 1.0 --expansion_ratio 100 --sampling_rate 0.2 --background_ratio 0 --sample_method unc --is_hybrid --note 1.0_0.2_0 &

# CUDA_VISIBLE_DEVICES=7 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/Hybrid_opv2v_vis --box_ratio 0.0 --expansion_ratio 100 --sampling_rate 0.0 --background_ratio 0 --sample_method unc --is_hybrid --note 0.0_0.0_0 &

CUDA_VISIBLE_DEVICES=3 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/Hybrid_opv2v_vis  --fusion_method late &

CUDA_VISIBLE_DEVICES=1 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/opv2v_point_pillar_lidar_multiscale_max_where2comm_2023_03_13_16_14_52 --fusion_method intermediate &