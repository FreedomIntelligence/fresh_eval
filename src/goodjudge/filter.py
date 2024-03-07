# filter the duplicate in gjo.jsonl
ans=[]
with open ('gjo.jsonl','r') as f:
    lines=f.readlines()
    # logger.info(f"crawler {crawler.__name__} done, total lines:{len(lines)}")
    seen = set()
    for line in lines:
        if line not in seen:
            seen.add(line)
            ans.append(line)
            # print(line)
with open ('gjo_no_dup.jsonl','w') as f:
    for line in ans:
        f.write(line)
        # f.write('\n')