

for i in  0.3 0.4 1 
do
  CUDA_VISIBLE_DEVICES=5 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/opv2v_where2comm_new --fusion_method intermediate_with_comm --note thr$i --thr $i &
done

for i in 0.25 0.35 0.1 0.5
do
   CUDA_VISIBLE_DEVICES=7 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/opv2v_where2comm_new --fusion_method intermediate_with_comm --note thr$i --thr $i &
done

for i in 0.45 0.15  
do
   CUDA_VISIBLE_DEVICES=2 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/opv2v_where2comm_new --fusion_method intermediate_with_comm --note thr$i --thr $i &
done

for i in 0.05 0.01 
do
   CUDA_VISIBLE_DEVICES=4 python opencood/tools/inference.py --model_dir /GPFS/data/yunqiaoyang/opv2v_where2comm_new --fusion_method intermediate_with_comm --note thr$i --thr $i &
done