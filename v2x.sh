for i in 0 0.005 0.01 0.05 0.1 0.2 0.5 1
do
  CUDA_VISIBLE_DEVICES=$1 python opencood/tools/inference.py --model_dir /GPFS/data/juntongpeng/hybrid-v2x/ --box_ratio $2 --expansion_ratio $3 --sampling_rate $i --sample_method unc --is_hybrid --note hybrid_exp_$3_unc_$2_$i
done