for i in 1.0 0.5 0.25 0.05 0.01 0.125 0.005 0.0
do
    python opencood/tools/inference.py --model_dir /GPFS/data/juntongpeng/Hybrid --sample_method unc --sampling_rate $i --note sampler_$i --sampler_path /GPFS/data/juntongpeng/Hybrid/2023-05-04-19-04-57/sampler/mix10LB5/best_sampler.pth
done