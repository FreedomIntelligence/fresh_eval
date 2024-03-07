# add two numbers
def add(a, b):
    return a + b

sss='''praw_reddit.jsonl                rq_arxiv_mathematics.jsonl  rq_arxiv_q_finance.jsonl   wr_Yahoo.jsonl              wr_quora_Movies.jsonl
rq_arxiv_computer_science.jsonl    rq_arxiv_statistics.jsonl  wr_bbc.jsonl                wr_quora_Technology.jsonl
rq_arxiv_economics.jsonl         rq_arxiv_physics.jsonl      rq_github.jsonl            wr_quora_Health.jsonl       wr_wiki.jsonl
rq_arxiv_eess.jsonl              rq_arxiv_q_biology.jsonl    rq_wattpad.jsonl           wr_quora_Mathematics.jsonl'''
expected_files =[i for i in sss.split() if i ]
print(len(expected_files),expected_files)
for i in expected_files:
    print(i,type(i),i=='')
    #   