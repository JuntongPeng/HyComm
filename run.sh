# for i in 0 0.01 0.05 0.25 0.5 0.75 1
# do
#   CUDA_VISIBLE_DEVICES=4 python opencood/tools/inference.py --model_dir /GPFS/data/juntongpeng/hybrid_early/ --sample_method unc --is_hybrid --sampling_rate $i --note _unc3_hybrid_uncNMS_$i
# done

for i in 0.8 0.9
do
  CUDA_VISIBLE_DEVICES=2 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/Hybrid_opv2v_pose_error/ --box_ratio 1.0 --expansion_ratio 100 --sampling_rate 0.2 --background_ratio 0 --sample_method unc --pose_index $i --is_hybrid --note 1.0_0.2_0 &

  CUDA_VISIBLE_DEVICES=2 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/Hybrid_opv2v_pose_error/ --box_ratio 1.0 --expansion_ratio 100 --sampling_rate 0.0 --background_ratio 0 --sample_method unc --pose_index $i --is_hybrid --note 1.0_0.0_0 &

done

for i in 0 0.1 
do
  CUDA_VISIBLE_DEVICES=7 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/Hybrid_opv2v_pose_error/ --box_ratio 1.0 --expansion_ratio 100 --sampling_rate 0.2 --background_ratio 0 --sample_method unc --pose_index $i --is_hybrid --note 1.0_0.2_0 &

  CUDA_VISIBLE_DEVICES=7 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/Hybrid_opv2v_pose_error/ --box_ratio 1.0 --expansion_ratio 100 --sampling_rate 0.0 --background_ratio 0 --sample_method unc --pose_index $i --is_hybrid --note 1.0_0.0_0 &
  
done

for i in 0.2 0.3 
do
  CUDA_VISIBLE_DEVICES=3 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/Hybrid_opv2v_pose_error/ --box_ratio 1.0 --expansion_ratio 100 --sampling_rate 0.2 --background_ratio 0 --sample_method unc --pose_index $i --is_hybrid --note 1.0_0.2_0 &

  CUDA_VISIBLE_DEVICES=3 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/Hybrid_opv2v_pose_error/ --box_ratio 1.0 --expansion_ratio 100 --sampling_rate 0.0 --background_ratio 0 --sample_method unc --pose_index $i --is_hybrid --note 1.0_0.0_0 &
  
done

for i in 0.4 0.5 
do
  CUDA_VISIBLE_DEVICES=4 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/Hybrid_opv2v_pose_error/ --box_ratio 1.0 --expansion_ratio 100 --sampling_rate 0.2 --background_ratio 0 --sample_method unc --pose_index $i --is_hybrid --note 1.0_0.2_0 &

  CUDA_VISIBLE_DEVICES=4 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/Hybrid_opv2v_pose_error/ --box_ratio 1.0 --expansion_ratio 100 --sampling_rate 0.0 --background_ratio 0 --sample_method unc --pose_index $i --is_hybrid --note 1.0_0.0_0 &
  
done

for i in 0.6 0.7 
do
  CUDA_VISIBLE_DEVICES=6 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/Hybrid_opv2v_pose_error/ --box_ratio 1.0 --expansion_ratio 100 --sampling_rate 0.2 --background_ratio 0 --sample_method unc --pose_index $i --is_hybrid --note 1.0_0.2_0 &

  CUDA_VISIBLE_DEVICES=6 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/Hybrid_opv2v_pose_error/ --box_ratio 1.0 --expansion_ratio 100 --sampling_rate 0.0 --background_ratio 0 --sample_method unc --pose_index $i --is_hybrid --note 1.0_0.0_0 &
  
done