python get_urls.py
# urls are saved at jgo.json  
python filter.py
# get no duplicates at gjo_no_dup.json
python crawl_urls.py
# use the urls in gjo_no_dup.json to crawl the data, saved in gjo.csv
# errors are in error.txt
python make_json_for_harness.py
# make json for harness in gjo.json

