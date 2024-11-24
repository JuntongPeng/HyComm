for i in 1.0 0.1 0.2 0.5 0 0.005 0.01 0.05 0.002 0.001 0.4 0.8
do
  CUDA_VISIBLE_DEVICES=$1 python opencood/tools/inference.py --model_dir /GPFS/data/juntongpeng/Hybrid_dairv2x/ --box_ratio $2 --expansion_ratio $3 --sampling_rate $i --sample_method unc --is_hybrid --note unc_nms_$3_unc_$2_$i
done